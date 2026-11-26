# Workstream N — the nesting theorem for the structure it uses: tail functions, instances, obstructions

Independent report on the brief `docs/workstreams/N_brief.md` (2026-11-26).  Paper proofs with numerical checks; no
Lean.  Created by this workstream: this file and `experiments/workstreams/N/` (a library and five scripts with their
stored outputs; commands in §7).  Nothing else in the repository was modified, no state-changing git command was
run, `lake` and `scripts/audit_all.sh` were not run, nothing was delegated.  Read for this report: the brief;
`THY-MSG-0016` §1;
theory report §11.16 (Lemma 11.43, Theorem 11.44, Proposition 11.46), §11.18 (bracket procedures, Theorems 11.52–11.54
with remarks), §11.19 (Lemma 11.55, Theorem 11.56 with its remarks, Proposition 11.57, statement of Theorem 11.58),
§11.20 (Theorems 11.59–11.64, Lemma 11.62, remarks), §11.21, §11.26 (Theorems 11.95–11.101), §11.32 (Theorem 11.116,
Proposition 11.117(a),(b)); `K_REPORT.md` errata and §§1–3; `R_brief.md`; `HintRecursion.lean` (the structure
`HintPair` only); `qlib.py`, `r8_flat.py` (tables), `K/sim_outer_loop.py` (its header).  **Not read:** the reports of
workstreams F, W, Y themselves (their statements are taken from the theory report), the referee reports, the Lean
files beyond the one structure, §§11.22–11.25 and 11.27–11.31.

**Status labels.**  **[proved here]** — a complete paper proof in this report, unrefereed (where a part is checked
numerically this is said); **[quoted: source, status there]** — taken from the theory report or `K_REPORT.md` with the
label it has there (`[V]` machine-checked, `[P]` paper, `[N]` numerical), or from the literature; literature that I
could not re-read is marked **quoted from memory, to be verified**; **[numerical]**; **[heuristic]**; **[sketch]**
(missing steps named); **[open]**.

**Notation.**  As in the theory report §11.16/§11.18 and `K_REPORT.md`: `Q_n`, `L_u`, `W`, `A`, `p_u`, `Λ₁`, `ε*`, `a`,
`h`, `θ_na`, `θ_hint`, `B(m,r)`, `E_r(m)`, `T_m(k)`, `Γ̃`, `Γ″`, `c_η = (1−η)/(1+η)`.  New here: an *envelope* `ρ` on a
space `X` is a function `ρ : X × X → [0, ∞]` with `ρ(x,x) = 0`; its class is `𝒱_ρ = {V > 0 : V(x) ≤ V(z)·e^{ρ(x,z)}}`
(for a Lipschitz class `{ψ : ψ(z) − ψ(x) ≤ d(z,x)}` and `V = e^{−ψ}` this is `ρ(x,z) = d(z,x)`; for a metric the order
does not matter).  `Φ` is the standard normal distribution function, `γ_n` the standard Gaussian measure on `ℝⁿ`.

---

## 0. Verdicts in one page

**N1 (audit; done).**  The proof of Theorem 11.56 uses the cube in 31 identifiable places (§1): 15 have a role in
validity or in the probability of the good event, 15 serve cost or termination only, and one (`s₀ ≤ W`) is not
needed at all.  Every validity use is an instance of four facts about an *outer integrand* `V` on a probability
space: independent sampling of outer points, certified brackets of `V(a)`, two tail inequalities, and a certified
a-priori bracket.  The brief's reading §2(a) is right in substance and incomplete in
three places (the lower tail function; what the trivial bracket is used for; atoms) — §8.

**N2 (abstract level theorem; done).**  Theorem N1 (§2.3) is Theorem 11.56 for an outer integrand `V` on any
probability space with: i.i.d. sampling, refinable brackets of `V(a)` with certified costs, an upper tail function
`Ξ` and a lower tail function `Θ` (`Θ(p) = p` is always admissible), an a-priori bound `ℓ₀ ≤ A` and a cap
`V ≤ V_max`.  Conclusion: the same bracket, the same failure probability, the same cost formula, with
`2^{−n_o}E_{r(q)}` replaced by `Ξ(q)`, the Harper term by `Θ(p̲)`, `(2p_u)^n` by a free `κ₀ ≤ 1`, `2un` by
`ln(V_max/s₀)`, and `π†` by the *closing level* `π_* = sup{π : Ξ(q) ≤ θ(1−η)ν₀·q and Ξ(q) ≤ θ·max(c_ηq, Θ(c_ηq)) for all
q < π}`.  Atoms and integrality of radii are not used.  With the cube's conventions every constant of Theorem 11.56
is reproduced exactly (10 parameter sets, §7.2); with its own conventions the theorem has a smaller `J` and the same
accuracy.  Variants: no cap on `V` (Theorem N1′: termination through the closing level; this is how the cube's proof
terminates); two blocks with a product measure (Theorem N3); dependence under a *class-relative* bounded influence
(Theorem N4); an abstract base family (Proposition N2); the exponent of one level and the assembly of the levels
for a family with a uniform tail profile (Corollary N5, Proposition N6).

**N3 (exponent level; done).**  Proposition N7: a tail profile `w` with `w(θ) + θ` nonincreasing (strictly on
`[0, a]`) yields a `HintPair` — the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` and every other field of the Lean
structure —, so the level recursion converges to `θ_hint = w^{−1}` (machine-checked theorem of the report, quoted).
If `w` is also convex, `J(t) = min_θ[θ + t·w(θ)]` is a game function in the sense of Theorem 11.66 and the dual
formulas of `R_brief.md` hold.  The condition on `w + id` is a hypothesis, not a tautology: without it the identity
fails (the transport profile, §3.1(c)).  Heterogeneous families: the recursion is stated for arbitrary splits of the
sites; no split undercuts the hinted exponent and the proportional split has it as a fixed point (Proposition N8,
proved); at two levels the best outer block is *not* proportional — it prefers the steep sites (numerical; `0.5051·a`
against `0.5129·a` in one example).

**N4 (instances; done, with the statuses of §4).**  Exact tail functions exist for the uniform cube (every `n`) and
for Gauss space with the Euclidean metric and — new here — with the sum metric (every `n`; atomless, unbounded);
tail functions that are sharp at the exponential scale for biased cubes and finite alphabets (the report's Theorems
11.63, 11.97(c), relative to the flat-histogram reference).  For site-dependent slopes, continuous sites and chains only
valid, non-sharp tail functions are available (a sorted-slope Harper bound, a ball-volume bound, a transport bound,
a transfer under bounded density); the transport bound is useless for this algorithm (its relative tail grows for
small sets), and concentration alone cannot replace isoperimetry for small sets.

**N5 (obstructions; done).**  (a) Gauss space with Euclidean-Lipschitz functions: exact tail functions (Theorem N9);
with a fixed split of the coordinates the level operator satisfies `R_G[T] ≥ max(T, Θ_na)` for every `T`, and — as a
statement about the algorithm, not only about its bound — every run on its good event draws at least
`(2K/(1+η))·exp((L − √(2x_out))²/2)` outer points at a linear instance whose gradient lies in the outer block
(Proposition N10).  Not excluded: random subspaces as blocks.  The hinted lower bound *does* hold in high dimension,
with dips on large balls instead of half-spaces (Proposition N11) — the report's remark that it "does not transfer"
is too pessimistic.  (b) Unbounded influence: an explicit known part (complete bipartite coupling of unnormalised
strength) and the additive residual `u|b|` for which (F2) fails by `e^{11.8}` against the assumed `e^1` on a 12+16
site instance; the algorithm returns an invalid bracket in 80 of 80 runs (the certified upper end below `A` by factors
of `300` and `3700`), and with the tail function of the true class it is valid at the cost of an enumeration
(Proposition N12).  (c) Unbounded oscillation: an exponential moment of the envelope is necessary and sufficient
for any finite certified upper bound; with it, and a closing level, the theorem holds without a cap (Proposition
N13, Theorem N1′).

**N6 (assumption table; done).**  25 entries (§6).  Counts by category (an entry can carry two labels): essential
6; required only by the present proof 7; convenience 6; replaceable by a weaker quantitative condition 7; removal
changes the complexity 7; removal makes the result false 3; "not known" is written where it is the truth (7
entries).

**Errors found** (§8): five corrections to the brief's sketch, two to the theory report's remarks (a stale sentence
on product measures; the remark on Gauss space), none in the proofs of Theorems 11.52 and 11.56.

**The weakest link** (§9): the assembly over the levels in the abstract setting (Proposition N6) is the induction of
`K_REPORT.md` §3.3 with substitutions that I checked step by step but did not rewrite in full, and the unbounded
variant N1′ has been run only on small Gaussian instances in which no level was left as negligible.

---

## 1. N1 — the audit of the proof of Theorem 11.56

Source: `K_REPORT.md` §2.1–§2.4 (Algorithm 2L⁺, Theorem K1, the nine steps), the theory report's statement of Theorem
11.56 and the proof of Theorem 11.52, with the errata.  "Validity" = needed for `L ≤ A ≤ U` on the good event or for
the probability of that event; "width" = needed for `U ≤ e^{x_out}L`; "term." = needed for the algorithm to stop;
"cost" = enters only the bound on the number of queries.  The last column says what stands in its place in §2.

| # | where | what of the cube is used | needed for | in the abstract theorem |
|---|---|---|---|---|
| 1 | setting | `Q_n = Q_o × Q_i`, uniform = product of uniforms, so `A = E_aW(a)` | validity | `A = ∫V dμ_o` (S1); product or disintegration (Theorems N3, N4) |
| 2 | step 1 of the algorithm | outer points i.i.d. uniform on `Q_{n_o}` | validity ((V2), (V3) are binomial) | i.i.d. from `μ_o` (S5) |
| 3 | (F1), Lemma K.2 | a fibre of a member of `L_u(Q_n)` is in `L_u(Q_{n_i})` | validity ((V1)), cost (`C_l`) | brackets of `V(a)` exist (S4) |
| 4 | (F2), Lemma K.2 | `W(a) ≤ e^{u·d(a,a′)}W(a′)`, term by term — uses that both fibre averages carry the same weights `2^{−n_i}` | validity | `V` obeys (TU), (TL) (S2) |
| 5 | Step 3 | Lemma 11.43(b): `|{W > s}| ≤ |B(n_o,r)|`, `r ≤ n_o − 1` ⟹ `E(W − s)₊ ≤ s·2^{−n_o}E_r` (Harper) | validity (upper end) | (TU) with `Ξ` |
| 6 | Step 3 | no closure at `r = n_o` (a point outside the super-level set is needed) | validity | `Ξ(q) = +∞` allowed; `Ξ(1) = +∞` necessarily |
| 7 | Step 2 | Lemma 11.43(c): `|{W ≥ t}| ≥ |B(n_o,k)|` ⟹ `E min(W,t) ≥ t·2^{−n_o}T_{n_o}(k)` (Harper) | validity of `ℓ ≤ A`; its *purpose* is cost (closure at bounded accuracy) | (TL) with `Θ`; `Θ = id` always valid |
| 8 | Step 2 | `|S| ≥ 2^{n_o}p(t)`: counting measure | validity of 7 | part of (TL) |
| 9 | step 0 | `s₀ = e^{−ψ₀−un} ≤ W` (oscillation `≤ un` around the reference point) | **not needed** for validity (`∫₀^{s₀}p ≤ s₀` holds for every `s₀`); used in Step 7 only through `ℓ ≥ s₀` | `s₀ = κ₀ℓ₀`, any `κ₀ ≤ 1` |
| 10 | step 0, Step 9 | `W ≤ s₀e^{2un}` | term. (above it nothing is high); the fallback bracket | cap `V_max` (S3), rule (c0); or no cap (Theorem N1′) |
| 11 | step 0, Step 2 | `ℓ₀ = e^{−ψ₀}((1+e^{−u})/2)^n ≤ A` (binomial sum of the lower cone) | validity of `ℓ ≤ A`; width (`s₀ ≤ (2p_u)^nL`) | `ℓ₀ ≤ A` (S3); `κ₀` in the width |
| 12 | step 1 | trivial bracket of a point, ratio `e^{2un_i}` | validity of rung 0; cost (top of the ladder) | rung 0 of (S4), `x₀` |
| 13 | step 2(c) | `tail := 0` if `2^{n_o}q < 1` (atoms of mass `2^{−n_o}`) | validity of that rule; term. | `Ξ(q) = 0` below the least atom is a property of `Ξ`; not needed |
| 14 | step 2(c) | "least radius with `|B(n_o,r)| ≥ 2^{n_o}q`" (integrality) | validity (via 5); cost (a factor `≤ n_o+1` in `q`) | `Ξ` evaluated at `q` itself |
| 15 | step 2(b) | "largest `k` with `|B(n_o,k)| ≤ max{1, 2^{n_o}p̲}`" | validity (via 7) | `Θ(p̲)` |
| 16 | constants | `J = ⌈(2un + b + n_o ln 2)/λ⌉` (oscillation and atom) | term., cost (also through `K`) | `J = ⌈ln(V_max/s₀)/λ⌉` |
| 17 | constants | `π† = 2^{−n_o}|B(n_o,r†)|`, `π† = 2^{−n_o−1}` if `r† = −1`; `m_max` | cost (also through `K`) | closing level `π_*` |
| 18 | §2.1 | `Γ̃(r) = E_r/|B(r−1)|`, `κ(r)`, `Γ″(r) = E_r/T(κ(r))` | cost (Step 5) | `Ξ(q)/q`, `Ξ(q)/Θ̄(c_ηq)` |
| 19 | Step 5 | minimality of `r`: `2^{n_o}q > |B(r−1)|`, hence `tail ≤ s_jqΓ̃(r)` | cost | none needed |
| 20 | Step 5 | `T_{n_o}(k)` nondecreasing in `k` | cost | `Θ` nondecreasing |
| 21 | Step 6 | `M₀^neg ≤ ν(2p_u)^n < ν` | cost | `νκ₀e^{−b} ≤ ν` |
| 22 | Step 7 | `ℓ_j ≥ s₀` (case `s_je^{−x} < s₀`) | cost (the count) | `κ₀ ≤ 1` |
| 23 | Step 9 | `s_Je^{−b} ≥ s₀e^{2un}2^{n_o} ≥ max W`; `M_J^neg ≥ K2^{n_o}/(1−η)`; then `q < 2^{−n_o}`, empty tail | term. | rule (c0), or Theorem N1′ |
| 24 | Step 9 | `A < s₀e^{2un}` strictly (the reference point has weight `s₀e^{un}`) | term. (strictness) | not needed |
| 25 | Theorem 11.52, good event | `M ≤ 4K·2^{n_o}` always, so the potential inner calls are a fixed finite set | probability | `M ≤ M̄` in every run (Step 6); as in Theorem K1 |
| 26 | Lemma 11.55 | ratios of binomial coefficients, the binomial median, Hoeffding, Stirling | cost (size of `π†`) | hypotheses on `Ξ/Θ` (§2.8, §4) |
| 27 | Corollary K1.b, (3.0) | `E_r ≤ e^{u(r+1)}(1+e^{−u})^m`, `|B(m,r−1)| ≥ (m+1)^{−1}e^{mH}` | cost (exponent) | uniform profile (U) |
| 28 | Proposition K0 | both tail lemmas for the base bracket | validity and cost of the base | Proposition N2 |
| 29 | Theorem 11.54, Proposition E | enumeration of `2^d` points as the fallback procedure; the rates `u`, `2u` | definition of a family; cost | (E0); any rate above the threshold |
| 30 | (11.18.2) | a block of `φn` coordinates is `Q_{φn}` with the same slope: the Hamming distance adds over blocks | cost (the factors `φ`, `1−φ`) — **the gain of nesting** | scale family (§2.8); fails for Euclidean Gauss space (§5.1) |
| 31 | remark on the lowered cap | `E_{r−1} ≤ e^{−u}E_r`, `E₁ ≥ (n_o+2)E₀`, `|B(r†)|/|B(r†−Δ)|` | cost (constant) | remark (R6) |

Not part of Theorems 11.52/11.56 but of 11.54/11.58: the lower bound, Theorem 11.25(a), uses the transitivity of
the cube (every query point lies in the same number of balls) — entry 24 of §6.

**What the audit shows.**  (i) Validity uses the cube only through entries 1–8, 11, 12, the validity halves of
13–15, and 25, 28: independent sampling, the product structure behind `A = E_aW`, (F1), (F2) *with its two tail
lemmas*, the certified numbers `ℓ₀` and the point bracket, and a bound on the number of potential inner calls.
(ii) The second tail lemma (entry 7) is absent from the brief's list; without it the algorithm is valid and is
Theorem 11.52 up to constants, with it the closure at a bounded accuracy becomes possible.  (iii) "Bounded oscillation" is three different things: a lower bound `ℓ₀` of `A` (always
available: `e^{−ψ₀}E e^{−d(x,x₀)}`), a bracket for each fibre average (an exponential moment on the inner block
suffices), and a cap on `V` (used for termination only, and replaceable — §2.5, §5.3).  `s₀ ≤ min W` is not needed.
(iv) Atoms are used in three places (13, 16/23, 17) and needed in none.  (v) The one use of the cube that is
"cost only" and nevertheless decides everything is entry 30.

---

## 2. N2 — the abstract level theorem

### 2.1 Tail functions

**Definition.**  Let `V > 0` be a measurable function on a probability space `(X, μ)`, `p(s) = μ(V > s)`,
`p̄(s) = μ(V ≥ s)`.  A function `Ξ : (0,1] → [0, ∞]` is an *upper tail function* of `V`, a nondecreasing
`Θ : (0,1] → [0,1]` a *lower tail function*, if for all `s > 0` and `q ∈ (0,1]`

    (TU)   p(s) ≤ q   ⟹   E(V − s)₊ ≤ s·Ξ(q),            (TL)   p̄(s) ≥ q   ⟹   E min(V, s) ≥ s·Θ(q).

Tail functions of a class are tail functions of all its members.  `Θ(q) = q` is a lower tail function of every `V`
(Markov), so `Θ̄(q) := max{q, Θ(q)}` is one whenever `Θ` is.  (TU) at `q = 1` forces `Ξ(1) = +∞` (let `s → 0`).  If
`μ` has no set of measure in `(0, q_at)`, then `Ξ` may be set to `0` on `(0, q_at)`.  `Ξ` may be replaced by its
nondecreasing hull `inf_{q′≥q}Ξ(q′)`; monotonicity of `Ξ` is not used below.

**Lemma N.0 (the tail functions of an envelope class) [proved here; for finite spaces the two inequalities are
Lemma 11.43(a) [V] and Lemma 11.62 [P] of the report at the zero reference].**  Let `ρ` be an envelope on `(X, μ)`
(`X` finite, or Polish with `ρ` continuous) and for a set `D` put `ρ(x→Dᶜ) = inf_{z∉D}ρ(x,z)`, `ρ(S→x) =
inf_{y∈S}ρ(y,x)`.  Then

    Ξ_ρ(q) = sup{ ∫_D (e^{ρ(x→Dᶜ)} − 1) dμ : μ(D) ≤ q, D ≠ X },        Θ_ρ(p) = inf{ ∫ e^{−ρ(S→x)} dμ : μ(S) ≥ p }

are tail functions of the class `𝒱_ρ`; if `ρ` satisfies the triangle inequality the dips `e^{ρ(x→Dᶜ)}` and
`e^{−ρ(S→x)}` are members and attain the integrals, so these are the least upper and the largest lower tail
function of the class.  Moreover `∫_D(e^{ρ(x→Dᶜ)} − 1)dμ = ∫₀^∞ e^r·μ{x : ρ(x→Dᶜ) > r} dr`.
*Proof.*  Let `V ∈ 𝒱_ρ`, `D = {V > s}`, `μ(D) ≤ q`, `D ≠ X`.  For `x ∈ D`, `z ∉ D`: `V(x) ≤ V(z)e^{ρ(x,z)} ≤ s·e^{ρ(x,z)}`,
so `V(x) − s ≤ s(e^{ρ(x→Dᶜ)} − 1)`; integrate over `D`.  For `S = {V ≥ s}`, `y ∈ S` and any `x`:
`s ≤ V(y) ≤ V(x)e^{ρ(y,x)}`, so `min(V(x), s) ≥ s·e^{−ρ(S→x)}`.  Membership of the dips is the triangle inequality:
`ρ(x→Dᶜ) ≤ ρ(x,z) + ρ(z→Dᶜ)`, `ρ(S→z) ≤ ρ(S→x) + ρ(x,z)`; the dip on `D` has `{V > 1} ⊆ D` and excess
`∫_D(e^{ρ(x→Dᶜ)} − 1)dμ`.  The last formula is the layer cake for `e^{ρ(x→Dᶜ)} − 1`.  ∎

So the tail functions are isoperimetric profiles of `(X, μ, ρ)`: `Ξ_ρ(q) ≤ ∫₀^∞e^r·α(q,r)dr` with
`α(q,r) = sup{1 − μ(A^r) : μ(A) ≥ 1 − q}`, `A^r = {x : ρ(x→A) ≤ r}`, and there is equality when the extremal sets are
nested (the cube: Harper; Gauss space: half-spaces, §5.1).  On a finite space both functions are finite optima over
subsets; `nlib.envelope_tails` computes them by enumeration for up to 16 points (§7.1, §7.3).

### 2.2 Setting and algorithm

**Setting (S).**
(S1) `(X_o, μ_o)` is a probability space, `V : X_o → (0, ∞)` measurable, `A := ∫V dμ_o < ∞`; `p`, `p̄` as above.
(S2) `Ξ`, `Θ` are tail functions of `V` under `μ_o`; `Θ̄ = max{id, Θ}`.
(S3) *Reference data.*  Numbers `0 < ℓ₀ ≤ A` and `V_max ≥ ℓ₀` with `V ≤ V_max` `μ_o`-almost surely, obtained with
`c_ref` queries; they are functions of the instance, not of the random choices.
(S4) *Brackets.*  Accuracies `x₀ > x₁ > … > x_L`, `L ≥ 1`, `x_L ≤ b`.  For every outer point `a`: rung `0` gives
`0 < L ≤ V(a) ≤ U ≤ e^{x₀}L` with at most `C₀` queries, always; rung `l ≥ 1` is a randomised procedure `I_l` that makes
at most `C_l` queries in every run and returns `L ≤ V(a) ≤ U ≤ e^{x_l}L` except with probability `δ′` — for every `a`,
with random bits independent of the outer points and of all other calls.
(S5) Independent points of law `μ_o` can be drawn; drawing costs no queries.

**Parameters:** `λ > 0`, `0 < η ≤ ½`, `η′ > 0`, `θ > 0`, `ν₁ ≥ 1`, `b > 0`, `0 < δ < 1`, `0 < κ₀ ≤ 1`.
**Constants:**

    s₀ = κ₀ℓ₀,   s_j = s₀e^{jλ},   J = ⌈ln(V_max/s₀)/λ⌉  (or any larger integer),   ν₀ = (1−η)^{−1}·max{(J+1)(e^λ−1)/η′, ν₁},
    π_* ∈ (0,1] any number such that for all 0 < q < π_*:     [N]  Ξ(q) ≤ θ(1−η)ν₀·q      and      [P]  Ξ(q) ≤ θ·Θ̄(c_ηq),
    m_max = ⌈log₂(2(1+η)e^λν₀/((1−η)π_*))⌉,     K = ⌈3(1+η)η^{−2}·ln(2(J+1)(m_max+1)(L+2)/δ)⌉,     ν = Kν₀,
    M† = K/((1−η)π_*),     M̄ = 2(1+η)e^λν₀M†,     δ′ = δ/(4L·M̄),     cnt(x) = max{K, 2(1+η)²(1−η)^{−1}e^λν·e^x},
    C_max = c_ref + 2M̄·C₀ + Σ_{l=1}^{L} min{2M̄, (J+1)·cnt(x_{l−1})}·C_l .

The supremum `π†` of the admissible `π_*` is the **closing level**; any smaller positive number gives a valid, weaker
theorem.

**Algorithm A** (Algorithm 2L⁺ of `K_REPORT.md` §2.2, with three substitutions marked ▶).
0. Reference data; `ℓ := ℓ₀`, `Σ := 0`.
1. Outer points `a₁, a₂, …` i.i.d. from `μ_o`, drawn when first needed; a new point gets its rung-0 bracket.
   Brackets are only refined: *to classify `a_i` at level `j`*, while `U_i > s_j` and `L_i ≤ s_je^{−b}` move `a_i` to
   the next rung, call `I_l` and intersect; then `a_i` is **low** if `U_i ≤ s_j`, **high** otherwise.
2. For `j = 0, 1, …`:
   ▶ (c0) if `s_j ≥ V_max`: **stop** and return `L = max{ℓ, Σ}`, `U = s₀ + Σ_{i<j}(s_{i+1} − s_i)q_i`.
   Otherwise `M := K` and repeat
   (a) classify `a₁..a_M` at level `j`; `N := #high`; `q := min{1, max(N,K)/((1−η)M)}`;
   (b) if `N ≥ K` (*populated*): `p̲ := N/((1+η)M)`, ▶ `ℓ := max{ℓ, s_je^{−b}·Θ̄(p̲)}`;
   (c) ▶ `tail := s_j·Ξ(q)`; if `tail ≤ θe^bℓ`: **stop** and return
       `L = max{ℓ, Σ + [N ≥ K](1−e^{−λ})e^{−b}s_jp̲}`, `U = s₀ + Σ_{i<j}(s_{i+1} − s_i)q_i + tail`;
   (d) else if `N ≥ K`: `q_j := q`, `p̲_j := p̲`, `Σ := Σ + (1−e^{−λ})e^{−b}s_jp̲`, next level;
   (e) else if `M ≥ M_j^neg := ν·s_j/(ℓ_je^b)` (*negligible*; `ℓ_j` the value of `ℓ` at the entry of level `j`):
       `q_j := q`, next level;
   (f) else `M := 2M`.
3. *Abort* with the bracket `[ℓ₀, V_max]`: before every query (a rung-0 bracket counted with `C₀`, a call of `I_l`
   with `C_l`) if it would take the count beyond `C_max`; if a point is unclassified at rung `L`; if `M` would exceed
   `K2^{m_max}`; or if a returned pair has `L > U`.

### 2.3 Statement

**Theorem N1 (one more level, abstract form) [proved here; the proof is that of Theorem K1 = 11.56 [P, refereed R8]
with the substitutions of §1; outer loop simulated on 2 624 runs in valid settings without a violation, §7.3].**
In the setting (S), with the constants of §2.2, Algorithm A makes at most `C_max` queries in every run and returns
`L ≤ U` with

    L ≤ A ≤ U,        U ≤ e^{x_out}·L,        x_out = ln[ κ₀ + e^b·( e^λ(1+η)/(1−η) + η′ + θ ) ],

except with probability `δ`.  More precisely there is an event `𝒢` of probability at least `1 − δ` on which
(i) no abort occurs and the algorithm stops at a level `j ≤ J`;
(ii) `L ≤ A ≤ U`, and every certificate is true: `p(s_i) ≤ q_i` at every level, `p(s_ie^{−b}) ≥ p̲_i` at every populated
one, `ℓ ≤ A` throughout;
(v) for every level `j` that is reached and every `x > 0`: `M_j^neg·p(s_je^{−x}) ≤ c_η^{−1}e^λ·ν·e^x`, and for
`x ∈ {x₀, …, x_{L−1}}` at most `cnt(x)` of the points used at level `j` have `V > s_je^{−x}`;
(vi) at most `min{M̄, cnt(x_{l−1})}` calls of `I_l` are made during one level, and the number of queries is at most
`c_ref + M̄C₀ + Σ_l min{M̄, (J+1)cnt(x_{l−1})}C_l`;
and *in every run, on or off `𝒢`*:
(iii) every level that is left without stopping has `q_j ≥ π_*`;
(iv) every sample size satisfies `M ≤ max{K, 2M_j^neg}`, `M_j^neg ≤ (1+η)e^λν₀M†`, hence `M ≤ M̄`;
(vii) a bracket returned through (c0) or (c) has `U ≤ e^{x_out}L`.

### 2.4 Proof

Write `X_t(M) = #{i ≤ M : V(a_i) > t}` and `ℳ = {K2^m : 0 ≤ m ≤ m_max}`.

**The good event** `𝒢 = (V1) ∩ (V2) ∩ (V3)`.  (V1): every potential call `(i, l)`, `i ≤ K2^{m_max}`, `1 ≤ l ≤ L` (its
random bits fixed in advance), returns a valid bracket of ratio at most `e^{x_l}`.  (V2): for all `0 ≤ j ≤ J`, `M ∈ ℳ`:
`Mp(s_j) ≤ K/(1−η)` or `X_{s_j}(M) ≥ (1−η)Mp(s_j)`.  (V3): for all `j`, `M` and `t ∈ {s_je^{−b}} ∪ {s_je^{−x_l} : 0 ≤ l ≤
L−1}`: `X_t(M) < K` or `X_t(M) ≤ (1+η)Mp(t)`.  The thresholds are functions of the reference data and the outer
points are independent of everything else (S3, S5), so `X_t(M)` is binomial `(M, p(t))` and the multiplicative
Chernoff bounds give each event of (V2), (V3) a failure probability at most `e^{−η²K/(3(1+η))}` (for (V3) with
`Mp(t) < K/(1+η)` by monotonicity in `p`); there are `(J+1)(m_max+1)(L+2)` of them, together at most `δ/2` by the
choice of `K`.  (V1) fails with probability at most `L·K2^{m_max}·δ′ < 2LM̄δ′ = δ/2` (condition on the outer points; S4).

**Step 1 (classification).**  At rung `L` the bracket has ratio `≤ e^{x_L} ≤ e^b`, so `U > s_j` implies
`L > s_je^{−b}`: classification ends at rung `L`.  On (V1) a point with `V > s_j` is never low and a high point has
`V > s_je^{−b}`: `X_{s_j}(M) ≤ N ≤ X_{s_je^{−b}}(M)`.
**Step 2 (certificates), on `𝒢`.**  `p(s_j) ≤ q` by (V2) as in `K_REPORT.md` Step 2.  If `N ≥ K` then
`X_{s_je^{−b}}(M) ≥ K`, so (V3) gives `p̲ ≤ p(s_je^{−b})`.  `ℓ ≤ A`: initially by (S3); with `t = s_je^{−b}`,
`p̄(t) ≥ p(t) ≥ p̲ > 0`, so (TL) for `Θ̄` gives `A ≥ E min(V,t) ≥ t·Θ̄(p̲)`.
**Step 3 (validity), on `𝒢`.**  `A = ∫₀^∞p(s)ds ≤ s₀ + Σ_{i<j}(s_{i+1} − s_i)p(s_i) + E(V − s_j)₊`; `p(s_i) ≤ q_i`; and
`E(V − s_j)₊ = 0` if `s_j ≥ V_max`, `≤ s_jΞ(q)` by (TU) otherwise.  Lower end: with `t_i = s_ie^{−b}` the intervals
`(t_{i−1}, t_i]` are disjoint and `p` is nonincreasing, so `A ≥ Σ_{i populated}(t_i − t_{i−1})p(t_i) ≥ Σ` (including
the current level if it is populated); and `ℓ ≤ A`.
**Step 4 (width; every run).**  `s₀ = κ₀ℓ₀ ≤ κ₀L`.  Populated levels: `q_i ≤ p̲_i/c_η`, so
`Σ_{pop}(s_{i+1} − s_i)q_i ≤ c_η^{−1}e^{λ+b}Σ ≤ c_η^{−1}e^{λ+b}L`.  Negligible levels: `q_i ≤ K/((1−η)M_i)` and
`M_i ≥ νs_i/(ℓ_ie^b)` give `(s_{i+1} − s_i)q_i ≤ (e^λ−1)e^bℓ/((1−η)ν₀) ≤ η′e^bℓ/(J+1)`, and at most `J+1` levels are
left.  `tail ≤ θe^bℓ`, or `tail = 0` under (c0).
**Step 5 (closing level; every run).**  Let level `j` be left at a pass `(M, N, q)`: the test failed,
`s_jΞ(q) > θe^bℓ`.  *Negligible:* `q ≤ K/((1−η)M) ≤ e^bℓ/((1−η)ν₀s_j)`, hence `Ξ(q) > θ(1−η)ν₀q`: [N] fails at `q`.
*Populated:* `q ≤ p̲/c_η`, so by monotonicity `Θ̄(c_ηq) ≤ Θ̄(p̲) ≤ e^bℓ/s_j` after the update (b), hence
`Ξ(q) > θΘ̄(c_ηq)`: [P] fails at `q`.  In both cases `q ≥ π_*`.
**Step 6 (sample sizes; every run).**  `M` is doubled only while `M < M_j^neg`.  A negligible level that is left
has `π_* ≤ q_j ≤ K/((1−η)M_j)`: `M_j ≤ M†`.  `M₀^neg = νκ₀e^{−b} ≤ ν ≤ ν₀M†`.  For `j ≥ 1`: after a negligible level,
`M_j^neg ≤ e^λM_{j−1}^neg ≤ e^λM_{j−1} ≤ e^λM†` (`ℓ` is nondecreasing); after a populated one,
`ℓ_j ≥ s_{j−1}e^{−b}p̲_{j−1} ≥ c_ηs_{j−1}e^{−b}q_{j−1}` and `q_{j−1} ≥ π_*`, so `M_j^neg ≤ νe^λ/(c_ηπ_*) = (1+η)e^λν₀M†`.
Hence `M ≤ M̄ ≤ K2^{m_max}`.
**Step 7 (the count), on `𝒢`.**  If `s_je^{−x} < s₀`: `M_j^neg·p ≤ νs_j/(ℓ_je^b) ≤ νs_j/s₀ < νe^x`, because
`ℓ_j ≥ ℓ₀ ≥ s₀` (`κ₀ ≤ 1`).  Otherwise let `i < j` be the largest index with `s_i ≤ s_je^{−x}` (`s_i > s_je^{−x−λ}`);
level `i` was left as populated (`s_iq_i ≤ s_ip̲_i/c_η ≤ e^bℓ_j/c_η`) or as negligible (`s_iq_i ≤ e^bℓ_j/((1−η)ν₀) ≤
e^bℓ_j`), and `p(s_je^{−x}) ≤ p(s_i) ≤ q_i`: `M_j^neg·p(s_je^{−x}) ≤ (νs_j/(ℓ_je^b))·e^bℓ_j/(c_ηs_i) < c_η^{−1}e^λνe^x`.
The second statement follows with (V3) at the last size `M_j < 2M_j^neg` (or `M_j = K`), as in `K_REPORT.md`.
**Step 8 (cost), on `𝒢`.**  A call of `I_l` for `a_i` during level `j` requires `U_i > s_j` at rung `l − 1`, where
`U_i ≤ e^{x_{l−1}}V(a_i)`: `V(a_i) > s_je^{−x_{l−1}}`.  With Step 7, each point being called at most once per rung, and
at most `J+1` levels: (vi).
**Step 9 (termination).**  Level `J` has `s_J ≥ V_max`, so rule (c0) stops the run there at the latest; within a
level the doubling is finite by Step 6.  On `𝒢` no abort occurs (Steps 1, 6, 8).  Off `𝒢` the abort rule keeps the
cost below `C_max` and returns a valid bracket (`ℓ₀ ≤ A ≤ V_max`).  ∎

The proof holds verbatim with any integer `J′ ≥ ⌈ln(V_max/s₀)/λ⌉` in place of `J` in the constants (it enters only
as a bound on the number of levels).

### 2.5 Remarks, variants, and the answers to the brief's questions

**(R1) Which properties of `Ξ`, `Θ` are used.**  Validity: (TU) and (TL), nothing else — not monotonicity, not
sharpness, not that `Ξ` is finite anywhere.  Cost: only the closing level, i.e. the two ratios `Ξ(q)/q` (levels
left as negligible) and `Ξ(q)/Θ̄(c_ηq)` (levels left as populated) on *all* `q` below it; and that `Θ` is
nondecreasing (Step 5).  A tail function that is too large costs evaluations, one that is too small costs validity.

**(R2) What replaces the atoms.**  Nothing is needed.  (a) *Termination* comes from the cap (rule (c0)).  The cube's
proof instead uses the atoms: Algorithm 2L⁺ has no rule (c0), `J_K = ⌈(2un + b + n_o ln 2)/λ⌉`, and at level `J_K`
nothing is high and `M_J^neg ≥ K2^{n_o}/(1−η)` forces `q < 2^{−n_o}`, an empty tail.  That argument is the special
case `π_* ≥ 2^{−n_o−1}` of Theorem N1′ below.  (b) *The number of outer points* is bounded by `M̄ ∝ 1/π_*` in every
run; on a space with a least atom `q_at` one has `π† ≥ q_at` automatically (`Ξ = 0` below it), which is the cube's
convention "`r† = −1`" improved by a factor `2`.  For a measure without atoms `π† > 0` iff the two ratios stay below
their thresholds as `q → 0` — true whenever `Ξ(q)/q → 0` (Gauss space: `Ξ_L(q)/q ~ L/(t−L)`), false for a tail
function such as the transport bound of §4(e), whose ratio grows as `q → 0`.  (c) *No enumeration* of the space is
available as a fallback; the base family of Proposition N2 takes its place.

**(R3) What replaces integrality of radii.**  Nothing: `Ξ` is evaluated at the certified `q`.  On the cube Harper's
`E_r` is the exact tail function at `q = |B(r)|/2^m` only; between ball sizes the exact function is that of the
segments of the simplicial order (Harper's theorem at every cardinality, and the neighbourhood of an initial
segment is one; verified against all subsets for `m ≤ 4`: §7.1 A3 **[numerical]**), and the step function used by
Algorithm 2L⁺ exceeds it by a factor up to `3.9` at `m = 4`, `u = 1` (`1/0.259`; §7.1 C, the row with equal slopes).
Using the segment values would be valid and slightly cheaper; no exponent changes.

**(R4) The cube as a special case — what the constants become.**

| abstract | cube (Theorem 11.56) |
|---|---|
| `(X_o, μ_o)`, `V` | `Q_{n_o}` uniform, `W(a) = 2^{−n_i}Σ_be^{−ψ(a,b)}` |
| `ℓ₀` | `e^{−ψ₀}((1+e^{−u})/2)^n` |
| `V_max` | `e^{−ψ₀+un}` (one could take `e^{−ψ₀+un_o}((1+e^u)/2)^{n_i}`) |
| `κ₀` | `(2p_u)^n` (so that `s₀ = e^{−ψ₀−un}`; any `κ₀ ≤ 1` is allowed) |
| `ln(V_max/s₀)` | `2un` |
| `Ξ(q)` | `0` for `q < 2^{−n_o}`; `2^{−n_o}E_{r(q)}(n_o)`, `r(q)` the least radius with `|B(n_o,r)| ≥ 2^{n_o}q`; `+∞` if `r(q) = n_o` |
| `Θ(p)` | `2^{−n_o}T_{n_o}(k(p))`, `k(p)` the largest radius with `|B(n_o,k)| ≤ max{1, 2^{n_o}p}` |
| `x₀`, `C₀`, `c_ref` | `2un_i` (the moment form `un_i` would do), `1`, `1` |
| `π_*` | `π† = 2^{−n_o}|B(n_o, r†)|`: the conditions [N], [P] in terms of `q` hold on a whole step `(|B(r−1)|, |B(r)|]·2^{−n_o}` iff the conditions of `K_REPORT.md` §2.1 hold at `r` |
| `J` | `⌈2un/λ⌉`; the cube's `⌈(2un + b + n_o ln 2)/λ⌉` is an admissible larger value |

With `J := J_K` and `π_* := π†` (`2^{−n_o−1}` if `r† = −1`) **every constant of Theorem N1 equals the corresponding
constant of Theorem 11.56** — `J`, `ν₀`, `r†`, `π†`, `m_max`, `K`, `M̄`, `δ′`, `x_out`, `C_max` — in all ten parameter sets
of §7.2 (bounded and extensive thresholds, `r† = −1` included), against workstream Q's evaluator; the algorithm
differs from 2L⁺ only by rule (c0), which can end a run earlier with the same guarantees.  With its own conventions
Theorem N1 has `J` smaller by `(b + n_o ln 2)/λ` and `ln C_max` smaller by `0.004` to `0.29` in those sets; `x_out` is
the same.  **The cube does come out as the special case, with the constants of Theorem 11.56.**

**Theorem N1′ (no cap on `V`) [proved here; run on Gaussian outer spaces, §7.4 G5].**  In the setting (S) let (S3)
be replaced by: numbers `0 < ℓ₀ ≤ A ≤ u₀` (no cap on `V`).  Run Algorithm A without rule (c0), with the abort
bracket `[ℓ₀, u₀]`, with `π_* > 0` such that `Ξ(q) ≤ θν₁·q` and [P] hold for all `q < π_*`, and with

    J = ⌊ ( ln(u₀/s₀) + b + λ + ln((1+η)/((1−η)π_*)) ) / λ ⌋

(the other constants as before; an abort also if level `J+1` would be entered).  Then all statements of Theorem
N1 hold.
*Proof.*  `θν₁ ≤ θ(1−η)ν₀`, so [N] holds below `π_*` and Steps 1–8 are unchanged (none uses the cap).  Termination:
by Step 6, in every run `M_j^neg ≤ (1+η)e^λν₀M†` at every level reached; on `𝒢`, `ℓ ≤ A ≤ u₀`, so
`M_j^neg = νs_j/(ℓ_je^b) ≥ νs_j/(u₀e^b)`; hence `s_j ≤ u₀e^{b+λ}(1+η)/((1−η)π_*)`, i.e. `j ≤ J`.  So on `𝒢` level `J+1`
is never entered, every level has finitely many passes, and the run ends by the closure test at a level `≤ J`.  ∎
The cube's `J_K` is of this form with `u₀/s₀ = e^{2un}` and `1/π_* ≤ 2^{n_o+1}`.

**(R5) An unconditional cap.**  In Theorem N1, every level below `J` has `M_j^neg ≤ ν·(V_max/ℓ₀)·e^{−b}`, so in
every run `M ≤ max{K, 2ν(V_max/ℓ₀)e^{−b}}` — with *no* tail function at all (`Ξ ≡ +∞`: the run climbs the whole
ladder and stops by (c0)).  This is the cost of the oscillation, `e^{D−b}` with `D = ln(V_max/ℓ₀)`, comparable to
Chebyshev for a variable of ratio `e^D`; everything a tail function buys is measured against it.

**(R6) The lowered cap, abstractly [proved here; 1 488 runs, largest sample `0.61` of it, §7.3].**  Let
`π‡ = sup{π : e^λΞ(q) ≤ θΘ̄(c_ηπ_*) for all q < π}` and `M‡ = K/((1−η)π‡)`.  *In every run every sample size is at
most* `max{K, 2Kν₀κ₀e^{−b}, 2e^λM†, 2M‡}`.  Proof: at level `0`, `M ≤ max{K, 2M₀^neg}`; after a negligible level
`M_j^neg ≤ e^λM†` (Step 6); after a populated level `j−1` (left, so `q_{j−1} ≥ π_*` and
`ℓ ≥ s_{j−1}e^{−b}Θ̄(c_ηπ_*)`), an unpopulated pass with `q < π‡` has `tail = e^λs_{j−1}Ξ(q) ≤ θe^bℓ` and stops, so `M`
is doubled only while `K/((1−η)M) ≥ π‡`.  ∎  On the cube `π‡ ≥ 2^{−n_o}|B(n_o, r† − ⌈λ/u⌉)|` by `E_{r−1} ≤ e^{−u}E_r`:
this is the report's remark after Theorem 11.56, without its case distinction at `r† < ⌈λ/u⌉`.

**(R7) A lower bound on the outer sample of this algorithm, instance by instance [proved here; 1 458 runs,
smallest ratio `3.5`, §7.3].**  Let `t_x = inf{t : E min(V,t) ≥ e^{−x_out}A}` and suppose `ℓ₀ < e^{−x_out}A`.  *On `𝒢`
the largest sample size of a run satisfies `M_max ≥ K/((1+η)·p(t_x − 0))`.*  Proof: on `𝒢`, `U ≥ A` and
`U ≤ e^{x_out}L`, so `L ≥ e^{−x_out}A`.  Let `t* = sup{t : p(t) ≥ K/((1+η)M_max)}`.  Every populated level has
`p(s_ie^{−b}) ≥ p̲_i ≥ K/((1+η)M_max)`, so `t_i = s_ie^{−b} ≤ t*`; then `Σ ≤ Σ_{pop}(t_i − t_{i−1})p(t_i) ≤ ∫₀^{t*}p =
E min(V, t*)`, and every update of `ℓ` is a lower bound of some `E min(V, t_i) ≤ E min(V, t*)`.  So
`e^{−x_out}A ≤ L ≤ max{ℓ₀, E min(V, t*)}`, hence `t* ≥ t_x`.  ∎  In words: the outer sample must reach the quantile
below which the truncated mean carries the fraction `e^{−x_out}` of `A` — whatever the tail functions, the inner
procedures and the parameters.  At a cone on the outer cube this is `e^{n_oθ_na(x_out/n_o)}` up to polynomial factors
(the referee's remark that `τ` is the exponent of the algorithm and not only a bound for it); it is the tool of §5.1.

**Proposition N2 (the base family, abstractly) [proved here; the proof is that of Proposition K0 [P]; coverage
simulated on Gauss space, §7.4 G7].**  Let `V > 0` on `(X, μ)` have tail functions `Ξ`, `Θ`; let `0 < η ≤ ½`, `K ≥ 1`,
`M ≥ K/(1−η)`, `q₊ = K/((1−η)M)`, `q₋ = K/((1+η)M)`.  Draw two independent samples of size `M`; let `t̂` be the `K`-th
largest value of `V` in the first and `Â` the mean of `min(V, t̂)` over the second.  Outside an event of probability
`4e^{−η²K/(3(1+η))}`

    L := Â/(1+η)  ≤  A  ≤  U := Â/(1−η) + t̂·Ξ(q₊),            U/L  ≤  ((1+η)/(1−η))·(1 + Ξ(q₊)/Θ̄(q₋)).

No bracket, no cap and no atom is needed; the cost is `2M` evaluations of `V`.  (Events: `p(t̂) ≤ q₊`,
`p̄(t̂) ≥ q₋`, and the relative error of `Â` at most `η`, each by a Chernoff bound as in `K_REPORT.md` §3.2 — the
thresholds `t^± = inf{s : p(s) ≤ q_±}` are defined for any law; then (TU) at `q₊`, (TL) at `q₋`.)

### 2.6 Two blocks with a product measure

**Theorem N3 [proved here: a verification of (S)].**  Let `(X_o, μ_o)`, `(X_i, μ_i)` be probability spaces, `𝒞` a
set of functions `ψ` on `X_o × X_i` with `A(ψ) = ∫e^{−ψ}d(μ_o ⊗ μ_i) < ∞`, queried by evaluation.  Suppose
(F1) there is a class `𝒞_i` on `X_i` containing every fibre `ψ(a, ·)`, `ψ ∈ 𝒞`, and bracket procedures `I_1..I_L` for
`(X_i, μ_i, 𝒞_i)` with accuracies `x_l`, failure probability `δ′` and costs `C_l` (in every run);
(F2) there are `Ξ_o`, `Θ_o` that are tail functions, under `μ_o`, of `V_ψ(a) = ∫e^{−ψ(a,b)}μ_i(db)` for every `ψ ∈ 𝒞`;
(B) from `c_ref` queries numbers `ℓ₀ ≤ A(ψ)`, `V_max ≥ sup V_ψ` (or `u₀ ≥ A(ψ)`) can be computed, and from `C₀` queries
on a fibre a bracket of `V_ψ(a)` of ratio at most `e^{x₀}`.
Then Algorithm A, run on `V_ψ` with points drawn from `μ_o` and `I_l` applied to the fibres, is a bracket procedure
for `(X_o × X_i, μ_o ⊗ μ_i, 𝒞)` with accuracy `x_out`, failure probability `δ` and cost `C_max` (Theorem N1 or N1′).
*For a Lipschitz class* `𝒞 = {ψ : ψ(z) − ψ(x) ≤ d(z,x)}` with a quasi-metric `d` on the product: (F1) holds with the
restrictions of `d` to the fibres, (F2) with the envelope `ρ_o(a,a′) = sup_b d((a′,b),(a,b))` and the functions of
Lemma N.0 (`V_ψ(a) ≤ V_ψ(a′)e^{ρ_o(a,a′)}` term by term), and (B) with `ℓ₀ = e^{−ψ(x₀)}∫e^{−d(x,x₀)}dμ`, a point bracket
`e^{−ψ(a,b₀)}·[∫e^{−d((a,b),(a,b₀))}μ_i(db), ∫e^{d((a,b₀),(a,b))}μ_i(db)]`, and `V_max` or `u₀` from the corresponding
upper integrals.  Nothing here asks the metric to be a sum over the blocks: that is needed for the *cost* (§2.8).

### 2.7 Dependence

**Theorem N4 (a known part that is not a product; bounded influence) [proved here; simulated: §7.3 S3, S6].**
Let `μ` be a probability measure on `X_o × X_i` with marginal `μ_o` on `X_o` and conditional laws `μ(·|a)`.  Let `𝒞`
be a set of functions on `X_o × X_i` and `𝒲 = {e^{−ψ(a,·)} : ψ ∈ 𝒞, a ∈ X_o}` its set of fibre weights.  Suppose
(F1′) for every `a` there are bracket procedures for `∫w dμ(·|a)`, `w ∈ 𝒲`, with accuracies `x_l`, failure probability
`δ′` and costs `C_l` — *the inner procedures must be valid under every conditional law*;
(F2′) `ψ(a′,b) − ψ(a,b) ≤ d_o(a′,a)` for all `b` (Lipschitz in the outer variable), and there is `ι ≥ 0` on
`X_o × X_o` with

    ∫ w dμ(·|a)  ≤  e^{ι(a,a′)} · ∫ w dμ(·|a′)        for all a, a′ ∈ X_o and all w ∈ 𝒲        (class-relative influence).

Then `V_ψ(a) := ∫e^{−ψ(a,b)}μ(db|a)` satisfies `A(ψ) = ∫V_ψdμ_o` and `V_ψ(a) ≤ V_ψ(a′)·e^{d_o(a′,a) + ι(a,a′)}`, i.e.
`V_ψ ∈ 𝒱_ρ` for `ρ(a,a′) = d_o(a′,a) + ι(a,a′)`; with tail functions of `𝒱_ρ` under `μ_o` (Lemma N.0, or any bounds),
reference data and point brackets, Algorithm A — outer points from `μ_o`, inner procedures under `μ(·|a_i)` — has
all the guarantees of Theorem N1 (N1′).
*Proof.*  Disintegration gives `A = ∫V_ψdμ_o`.  `V_ψ(a) = ∫e^{−ψ(a,b)}μ(db|a) ≤ e^{d_o(a′,a)}∫e^{−ψ(a′,b)}μ(db|a) ≤
e^{d_o(a′,a)+ι(a,a′)}∫e^{−ψ(a′,b)}μ(db|a′)`, the last step by the influence bound for `w = e^{−ψ(a′,·)} ∈ 𝒲`.  The rest
is Theorem N1.  ∎
*Sufficient:* `dμ(·|a)/dμ(·|a′) ≤ e^{ι(a,a′)}` pointwise (the brief's hypothesis, with `ι = L·d_o`).  The
class-relative form is what is sharp: for `μ(·|a) = Bernoulli(p(a))^{⊗k}` and `u`-Lipschitz fibres,
`ι(a,a′) = k·max_± ln[(1 + p(a)(e^{±u}−1))/(1 + p(a′)(e^{±u}−1))]` (change one coordinate at a time; the conditional
expectations stay log-`u`-Lipschitz), attained by the uniform field; in §7.3 S3 the largest observed slope of
`−ln V` equals `u + k·ι₁` to four digits (`1.3120`, `0.7980`, `1.2721`) where the pointwise bound gives `1.754`,
`2.425`, `1.697`.  For a nearest-neighbour chain see §4(f).

**Lemma N18 (tail functions under a change of measure) [proved here; two lines].**  (a) If `e^{−c₁}ν ≤ μ ≤ e^{c₂}ν`
and `Ξ_ν` is an upper tail function of `V` under `ν`, then `q ↦ e^{c₂}Ξ_ν(e^{c₁}q)` is one under `μ`
(`μ(D) ≤ q ⟹ ν(D) ≤ e^{c₁}q`, and `∫(V−s)₊dμ ≤ e^{c₂}∫(V−s)₊dν`).  (b) *Reference instance (Lemma 11.62 [P] in this
language).*  If the points are drawn from `ν_o` with a known density `r = dμ_o/dν_o`, apply Theorem N1 to
`V̂ = r·V` under `ν_o`: brackets of `V̂(a)` are `r(a)` times brackets of `V(a)`, and `V ∈ 𝒱_ρ` gives
`V̂ ∈ 𝒱_{ρ̂}`, `ρ̂(x,z) = ρ(x,z) + ln r(x) − ln r(z)` (nonnegative when `ν_o` is the Gibbs law of a member of the
class: the slack of §11.20).

### 2.8 The exponent of one level, and the levels assembled

**Scale families.**  A *scale family* gives for every `m ≥ 1` a problem `(X_m, μ_m, 𝒞_m)` such that for
`n = n_o + n_i`: `X_n = X_{n_o} × X_{n_i}`, `μ_n = μ_{n_o} ⊗ μ_{n_i}`, (F1) with `𝒞_i = 𝒞_{n_i}`, (F2) with an upper tail
function `Ξ_{n_o}` that depends on `n_o` only, (B) with `ln(V_max/ℓ₀) ≤ d̄n` (or `ln(u₀/ℓ₀) ≤ d̄n`) and `x₀ ≤ ξ₀n_i`,
(E0) some bracket procedure of finite cost for every `(n, x, δ′)`, and

    (U)   there is a continuous nonincreasing x̄ : (0, ∞) → [0, ∞), bounded, such that for all θ₁ > 0, ε > 0 and
          all m ≥ m₀(θ₁, ε):     Ξ_m(q) ≤ q·exp( m·[ x̄(m^{−1} ln(1/q)) + ε ] )     for every q ≤ e^{−mθ₁}.

`θ_na(x) := inf{θ > 0 : x̄(θ) ≤ x}`.  (U) is one-sided and uniform over *all smaller* sets — the closing level is a
supremum over `q′ ≤ q` — and it cannot be asked up to `q = 1`: on the cube `Ξ_m(q)` for `q ≥ ½` has exponents up to
`u − Λ₁ > ε*`, and the convergence is only `O(√(ln m/m))` near `θ = 0` (§7.5 P1: `sup|w_m − w| = 0.062, 0.030, 0.015,
0.005` at `m = 100, 400, 1600, 12800`, `u = 1`).  The cube satisfies (U) with `x̄(θ) = KL(ρ‖p_u)`, `KL(ρ‖½) = θ`
(`0` from `a` on) by (3.0) of `K_REPORT.md`.

**Corollary N5 (the exponent of one level) [proved here; Corollary K1.b [P] with (U) in place of (3.0)].**  Let a
family of bracket procedures of a scale family have the exponent function `T`.  Fix `0 < φ < 1`, rates
`ξ₀ > ξ₁ > … > ξ_L > 0`, `G > (1−φ)ξ_L` and `c > 0`, and run Algorithm A in dimension `n` with `n_o = ⌊φn⌋`,
`x_l = ξ_ln_i`, `b = x_L`, `λ = 1`, `η = ½`, `η′ = 1`, `ν₁ = 1`, `κ₀ = 1`, `Θ = id`, `δ = e^{−cn}` and
`θ := e^{Gn−b} − (3e+1) − e^{−b}` (positive for large `n`).  Then the accuracy is exactly `Gn` and

    limsup_n n^{−1} ln C_max  ≤  max{ μ ,  max_{1≤l≤L} [ min(μ, (1−φ)ξ_{l−1}) + (1−φ)T(ξ_l) ] },        μ = φ·θ_na( ((G − (1−φ)ξ_L)/φ) − 0 ).

*Proof.*  `e^λ(1+η)/(1−η) + η′ = 3e + 1`, so `x_out = Gn`.  [P] holds at `q` as soon as `3Ξ(q) ≤ θq` (`Θ̄(q/3) ≥ q/3`),
and then [N] holds (`(1−η)ν₀ ≥ 1`).  `ln θ = n_o(e_∞ − o(1))`, `e_∞ = (G − (1−φ)ξ_L)/φ`.  Fix `ε > 0` and put
`θ₁ = θ_na(e_∞ − 3ε) + ε`; for `q ≤ e^{−n_oθ₁}`, (U) and the monotonicity of `x̄` give
`Ξ(q)/q ≤ exp(n_o[x̄(θ₁) + ε]) ≤ exp(n_o[e_∞ − 2ε]) ≤ θ/3` for large `n`.  So `π_* = e^{−n_oθ₁}` is admissible,
`M̄ = poly(n)/π_*`, and `limsup n^{−1}ln M̄ ≤ φ(θ_na(e_∞ − 3ε) + ε)`; let `ε → 0`.  The rest is claim (vi) with
`J, K, ν₀ = O(n)`, `cnt(x) = poly(n)e^x`, `n_i/n → 1−φ` and `δ′ ≥ e^{−c′n_i}`.  ∎

**Proposition N6 (the levels assembled: an adaptive upper bound from a tail profile) [the reduction: proved here
by checking Proposition E of `K_REPORT.md` §3.3 [P] step by step; the convergence of the recursion: quoted,
`iterates_lt_hint_add` [V]].**  Let a scale family satisfy (U) with a profile as in Proposition N7(a) below
(`x̄ = w + id`, strictly decreasing where positive), `E = x̄(0+)`.  Then for every `0 < ξ < E` and `η > 0` there is a
family of bracket procedures whose exponent at the rate `ξ` is at most `θ_hint(ξ) + η`: **adaptive algorithms without
a hint cost at most `exp(n·θ_hint(ξ) + o(n))` at the accuracy `ξn`**, `θ_hint = w^{−1}`.
*Steps checked.*  (1) Base family: Proposition N2 with `Θ = id`, `η = ½` and (U) has the exponent function `θ_na`
on `(0, ∞)` (closing `q = e^{−d(θ_na(ξ−2ε)+ε)}`; `θ_na` is continuous).  (2) The induction `k → k+1` of Proposition
E uses: the choice of `(φ, β)` with `S ≤ T_{k+1}(g) + ζ/4` (definition of the recursion); a ladder
`y_L < … < y_1 < ξ₀` with `y_L = min(β/(1−φ), ū)` — the cube's `u` and `2u` are any rate `ū` with `E < ū < ξ₀`, and
`ξ₀` may be enlarged at will (a wider trivial bracket is still valid); the pointwise cheapest of finitely many
families (general); Corollary K1.b — here Corollary N5; `T_k(y) ≤ θ_na(y) = 0` for `y ≥ ū > E` (definition of
`θ_na`); "enumeration for the remaining `(d, x, δ′)`" — here (E0).  (3) Statement (R) for the pair of the profile:
Proposition N7(a) and the machine-checked theorem.  No other property of the cube occurs in §3.3 of `K_REPORT.md`.
*Not rewritten in full here* — the weakest link of this report (§9).

Whether `θ_hint = w^{−1}` is the *true* adaptive exponent is a separate matter: it needs the tail profile to be
sharp and a lower bound of the hinted kind, which on the cube is Theorem 11.25(a) and uses its symmetry.

---

## 3. N3 — the exponent level

### 3.1 The pair of a tail profile

**Proposition N7 [proved here].**  Let `w : [0, θ̄] → ℝ` be continuous (`θ̄ ≤ ∞`; for `θ̄ = ∞` read `[0, ∞)`), and
`x(θ) := w(θ) + θ`.  Assume
(P0) `E := w(0) > 0`;
(P1) `x` is nonnegative and nonincreasing, and there is `a ∈ (0, θ̄]` with `x(a) = 0` and `x` strictly decreasing on
`[0, a]`.
Define `θ_hint := w^{−1}` on `[w(θ̄), E]` and `θ_na(x) := min{θ : x(θ) ≤ x}` for `x ≥ 0`.
(a) `w` is strictly decreasing with difference quotients `≤ −1`; `θ_hint` is continuous, strictly decreasing and
`1`-Lipschitz; `θ_na` is continuous, nonincreasing, `θ_na(0) = a`, `θ_na = 0` on `[E, ∞)`; and

    θ_na( e + θ_hint(e) )  =  θ_hint(e)        for −a ≤ e ≤ E.

With `h := θ_hint(0) ∈ (0, a)`, the pair satisfies every field of the Lean structure `HintPair θ_na θ_hint a h E`
(`HintRecursion.lean`): `0 < h`, `0 < a`, `θ_na ≤ a` and continuous on `(0, ∞)`, `θ_na(h) = h`, the identity on `(0, E)`,
`θ_hint > 0` there, `e + θ_hint(e)` nondecreasing, `θ_hint(e) ≥ h − e`.  Hence, by `iterates_lt_hint_add` and
`exactRec_reaches_hint_of_pair` **[quoted: theory report §11.18, §11.20, V]**, the level recursion built on `θ_na`
comes within every `η > 0` of `θ_hint` on `(0, E)`.
(b) If in addition (P2) `w` is convex, then `θ_hint` and `θ_na` are convex, and

    J(t) := min_θ [ θ + t·w(θ) ]        (0 ≤ t ≤ 1)

is concave, continuous, `J(0) = J(1) = 0`, `0 ≤ J(t) ≤ min{E·t, a·(1−t)}`, `sup_{t>0}J(t)/t = E` — a *game function*
in the sense of Theorem 11.66 **[V]** with the constants `E` and `L = a` — and

    θ_hint(e) = max_{0≤t≤1} [ J(t) − te ]   (−a ≤ e ≤ E),        θ_na(x) = sup_{0≤τ<1} ( J(τ) − τx )/(1 − τ)   (0 < x ≤ E).

So the pair of (a) is the pair of Theorem 11.66 for `F = J`, the tangent lines of `θ_na` are `(B, s)` with
`B = (1+s)J(s/(1+s))`, and `J″ = −1/θ_hint″` at corresponding points when both exist: the inputs of `R_brief.md` §2.
(c) *Neither (P1) nor (P2) is automatic.*  Without (P1) the identity fails; without (P2) the pair of (a) is still
a `HintPair`, but `J` sees only the convex hull of `w`.
*Proof.*  (a) `w(θ′) − w(θ) = x(θ′) − x(θ) − (θ′ − θ) ≤ −(θ′ − θ)` for `θ′ > θ`; the statements on the inverses follow,
`θ_na` being the inverse of `x` on `[0, a]` and `0` beyond `E = x(0)`.  For `−a ≤ e ≤ E` put `θ* = θ_hint(e) ∈ [0, a]`
(`w(a) = −a ≤ e ≤ w(0)`): `x(θ*) = e + θ*` and `x` is strictly decreasing on `[0, a]`, so `θ_na(e + θ*) = θ*`.  The
fields: `w(a) < 0 < w(0)` gives `h ∈ (0, a)`; `x(h) = h`; `e + θ_hint(e) = x(θ_hint(e))` is nondecreasing in `e`, whence
`θ_hint(e) ≥ h − e`.  (b) Inverses of decreasing convex functions are convex.  `θ + t·w(θ) = (1−t)θ + t·x(θ) ≥ 0`;
`θ = 0` and `θ = a` give the two upper bounds; `J(t)/t → w(0)` as `t → 0` by continuity.  For the first formula,
Sion's theorem (convex and continuous in `θ` on a compact interval — for `θ̄ = ∞` restrict to `[0, a]` —, linear in
`t ∈ [0,1]`) gives `max_t min_θ[θ + t(w(θ) − e)] = min_θ[θ + (w(θ) − e)₊]`, and for `θ < θ*` the bracket is
`x(θ) − e ≥ x(θ*) − e = θ*`.  For the second, with `s = τ/(1−τ)`: `(J(τ) − τx)/(1−τ) = min_θ[θ + s(x(θ) − x)]`, and
Sion again gives `sup_{s≥0} = min{θ : x(θ) ≤ x}`.  (c) is §7.5 P3 and the next paragraph.  ∎

**The hypotheses the brief asks about.**  *Existence of the limit* `w(θ) = lim (1/m)ln Ξ_m(e^{−mθ})` is not needed for
an upper bound: (U) of §2.8 asks only for an upper profile, uniformly over smaller sets; the limit — and its
agreement with a lower bound — matters for sharpness.  *Monotonicity:* `w` is nonincreasing because `Ξ_m` is; what is
needed is the stronger (P1).  *Convexity of `θ_na`*, of `θ_hint`, and everything `R_brief.md` uses of `J` come from (P2),
the convexity of `w`; a sharp profile is convex because a hinted lower bound is the transform of a game function,
so non-convexity signals a tail function that is not sharp.

**What this says about the brief's §2(b).**  "The identity holds by construction" is true exactly under (P1): the
relative tail exponent `x = w + id` — the exponent of `Ξ(q)/q` — must not increase as the set gets smaller, i.e.
`w′ ≤ −1`.  On the cube `w′ = −u/ln((1−ρ)/ρ) ≤ −1` with equality from `ρ = p_u` on (§7.5 P2: all fields to `10⁻⁹`,
`u ∈ {½, 1, 2, 4}`).  For a tail function that is valid but not sharp it can fail: the transport profile
`w_T(θ) = u²/8` (`θ ≤ u²/8`), `u√(θ/2) − θ` beyond (§4(e)) has `x_T` *increasing* from `u²/8` to `u√(ln 2/2)`; then
`θ_hint,T(0) = u²/2`, but the closing condition at the accuracy `e + θ_hint,T(e)` fails for all smaller sets down
to the atom (§7.5 P3) — the exponent of the level is `ln 2`, not `θ_hint,T`.  The closing level of the algorithm is
governed by the hull `sup_{θ′≥θ}x(θ′)`, which is why `θ_na` was defined through `x̄` in §2.8.  And "the non-adaptive
exponent" obtained this way is the exponent of *the base family of this method*; that no non-adaptive algorithm
does better is a separate theorem (11.45 on the cube).

### 3.2 Heterogeneous families

Sites of kinds `j = 1..m`; a block is a vector `β ∈ ℝ₊^m` (numbers of sites of each kind, per `n`).  Suppose every
block has a game function `J_β` on `[0,1]` that is **additive**, `J_{α+β} = J_α + J_β`, with hinted and non-adaptive
exponents (total units, per `n`)

    R̂_β(e) = max_{0≤t≤1}[J_β(t) − te],        Θ_na^β(x) = sup_{0≤τ<1}(J_β(τ) − τx)/(1 − τ).

This is the situation of §11.26: `F*(t) = Σ_jλ_jF*_j(t)` "with one common `t`" (Theorem 11.98(b) **[quoted, P]**) and
`θ_na^λ(x) = sup_τ(F*_λ(τ) − τx)/(1−τ)` (display (L) of Theorem 11.101).  An exponent function is now a function
`T(β; G)` of a block and a total accuracy, homogeneous of degree one.  **The level recursion** for the block `ν`:

    R[T](ν; G)  =  inf_{α + β = ν, 0 < B < G}   sup_{γ ≥ B} [ min(γ, Θ_na^α(G − B)) + T(β; γ) ],

the infimum over all ways of giving the outer block `α_j` of the `ν_j` sites of kind `j`.  For `α = φν` it is
(11.18.2).  Theorem 11.101 uses proportional splits only ("the outer block takes a fraction `φ` of the sites of
every type").

**Proposition N8 [proved here].**  Assume that `β ↦ J_β` is additive and positively homogeneous and `J_β(1) = 0`.
(a) *No split undercuts the hinted exponent:* for all `α + β = ν` and `0 < B < G`, with `μ = Θ_na^α(G − B)` and
`γ₀ = max(B, μ)`: `min(γ₀, μ) + R̂_β(γ₀) ≥ R̂_ν(G)`.  Hence `T(β;·) ≥ R̂_β` for all `β` implies `R[T](ν;·) ≥ R̂_ν`.
(b) *The proportional split has `R̂` as a fixed point:* if `(Θ_na^ν, R̂_ν)` obeys the shear identity and
`e + R̂_ν(e)` is nondecreasing, then `α = φν` with `φ = G/(G + R̂_ν(G))`, `B → 0` gives `R[R̂](ν; G) ≤ R̂_ν(G)`.
So the general recursion and the proportional one have the same limit, `R̂_ν` — in the limit of many levels it
does not matter which sites the outer block takes.
*Proof.*  (a) For `0 ≤ t < 1`: `J_α(t) ≤ (1−t)μ + t(G − B)` by the definition of `μ`, and `J_β(t) ≤ R̂_β(γ₀) + tγ₀`.
Adding, `J_ν(t) − tG ≤ μ + R̂_β(γ₀) + t(γ₀ − B − μ) ≤ μ + R̂_β(γ₀)` because `γ₀ ≤ B + μ`; at `t = 1` the left side
is `−G`.  (b) is Theorem 11.53(b) "`≤`" for the pair of the block `ν`: the outer exponent is `φΘ_na^ν(G/φ) = φR̂_ν(G)`,
and for `γ ≤ μ` the bracket is `(1−φ)S(γ/(1−φ)) ≤ (1−φ)S(G) = R̂_ν(G)`, for `γ ≥ μ` at most `φR̂_ν(G) + (1−φ)R̂_ν(G)`.  ∎
(a) holds numerically with margin on 1 200 random splits of three two-kind families (§7.5 P5).

**Which sites should the outer block take? — at finitely many levels, not a proportional share [numerical].**  For
two kinds of binary sites with slopes `u₁ > u₂` (uniform measure, `J_j(t) = Λ(tu_j) − tΛ(u_j)`), the two-level value
at vanishing accuracy, `τ₂(α) = max{a_β, sup_γ[min(γ, a_α) + Θ_na^β(γ)]}`, minimised over all splits against
proportional ones (§7.5 P5; grids of `41 × 41` splits):

| slopes, fractions | `a` | `h` | proportional | best split | outer block |
|---|---|---|---|---|---|
| `(2, 0.5)`, `(½, ½)` | `0.17906` | `0.05246` | `0.5083·a` | `0.5046·a` | `52 %` of the steep, `18 %` of the flat sites |
| `(3, 1)`, `(0.3, 0.7)` | `0.22835` | `0.07204` | `0.5129·a` | `0.5051·a` | `75 %` of the steep sites, none of the others |
| `(1.5, 0.25)`, `(½, ½)` | `0.11292` | `0.03123` | `0.5033·a` | `0.5019·a` | `50 %` steep, `45 %` flat |

The outer block prefers the steep sites: it pays the capacity `a_α` of what it takes, and what it leaves must
become easy at the accuracy `a_α`; flat sites have the smallest ratio of threshold to capacity (`E_j/a_j → 1` as
`u_j → 0`), so an inner block of flat sites drops fastest.  The gain is about one per cent of `a` at two levels.
**Flagged, not proved:** (i) the one-level theorem for non-proportional blocks needs the tail profile of every
sub-composition, uniformly — available in principle from Theorem 11.97(c), which is uniform over compositions, and
from the Lipschitz bound (L) of Theorem 11.101, but families "indexed by compositions" would have to carry exponent
functions on the whole simplex, and the induction (G1)–(G2) was written for inner blocks near `λ` **[sketch]**;
(ii) whether non-proportional splits improve the *rate* of the recursion (the constant `2π²h²θ_hint″(0)` of
Conjecture R) **[open]**; (iii) for families without additive game functions (interactions) nothing is claimed.

---

## 4. N4 — instances

"Sharp" means: the tail function has the profile whose inverse is the hinted lower bound.  "Gives" = what Theorem
N1 and Propositions N2, N6 add to what the report has.

| instance | spaces, class | tail function, source | sharp at the exponential scale? | status of the level theorem / exponents |
|---|---|---|---|---|
| (a) cube | `Q_m` uniform, `u`·Hamming | Harper's `E_r`, `T_k` (Lemma 11.43(b),(c) **[P + K]**; Harper's theorem cited) | yes, and exact at every `n` (at every cardinality with segments, §2.5 R3) | Theorem 11.56 with identical constants (§7.2); exponents: report |
| (b) biased cube | `Q_m`, `Bernoulli(p)^m`, sampled from `μ_H`, `V̂ = W/w_H` | `Ξ_H` of Lemma 11.62 **[P]**: a finite maximum, no closed form; exponent Theorem 11.63 **[P, refereed R9]** | yes (with Theorem 11.59(a)) | level theorem: now a corollary of a written theorem (Lemma N18(b) + N1); exponents: report; bounded accuracy **open** |
| (c) alphabets, site types | `Π𝒮_{τ(i)}`, product law, sum of site envelopes | as (b): Theorem 11.97(c) **[P, reviewed]**, uniform in the composition | yes (with Theorem 11.101(a)) | as (b) |
| (d) site-dependent slopes | `Q_m` uniform, `Σu_i[x_i ≠ y_i]` | finitely many slopes: (c).  Explicit, every `n`: sorted-slope Harper bound (Lemma N14, here) | (c): yes.  Lemma N14: **no** | valid for every `n` with N14; exponent of a continuum of slopes: Proposition N19 (here, given 11.101) |
| (e) continuous sites, bounded diameter, sum metric | e.g. circles | ball-volume (N15) and transport (N16) bounds, here; via discretisation (N17) the exponents of (c) | N15, N16: **no** (proved on the cube); N16 useless for closing | valid level procedure for every `n`; upper bound `R̂^{(k)}(ε₁ − 2πū/k)`; lower bound not proved |
| (e′) Gauss space, sum metric | `ℝ^m`, `γ_m`, `c`·`ℓ₁` | `Ξ_{c√m}`, `Θ_{c√m}` of Theorem N9 — **exact for this class** (here) | as a tail function: exact, every `n`.  A matching lower bound: **open** | Theorem N1′ applies; adaptive upper bound = the Gaussian pair exactly (Proposition N6) |
| (f) nearest-neighbour chain | segment, chain marginal; one-sided slack at the boundary site | finite maximum (Lemma N.0); transfer from block products (N18) | not available | validity of nesting without cutting the chain: here (Theorem N4); exponents: nothing beyond Theorem 11.116(f) |

**(a) The cube.**  Nothing to add to §2.5 (R3), (R4).

**(b), (c) Product measures and alphabets.**  In the report the upper bounds are "the two-level algorithm of
Theorem 11.52 relative to the reference `H`" (Theorem 11.64(i)) and a list of changed steps (Theorem 11.101).  With
Lemma N18(b) both are Theorem N1 for `V̂ = Z_H·W/w_H` under `μ_H` on the outer block, with any upper bound of `Ξ_H`
that vanishes below the least point mass: the changed steps become hypotheses that are checked once.  Two things
this gives: (1) repair (M2) of §11.20 is not needed — in Theorem N1 the union bound runs over at most `2LM̄` potential
calls, not over `4K/min μ_H`; (2) the accuracy of a level is the explicit `x_out`, without the term `ln(4eJ + 3) =
O(log n)` of Theorem 11.52 — what remains is `ln θ`, and `θ` is limited from below by the precision of the tail
function.  What it does **not** give is a bounded accuracy: that needs `Ξ(q) ≤ θ·Θ̄(c_ηq)` with a bounded `θ` for
all `q` down to `e^{−n_o(a+o(1))}`, a two-sided statement with polynomial precision at the critical scale; Theorem
11.63 has the slack `e^{nω_n}`, `ω_n ~ n^{−1/8}` from its proof, so a level closes only at accuracies `≫ n^{7/8}`.  The
abstract theorem names the missing object (the analogue of Lemma 11.55(b) for `Ξ_H` and a lower tail function of
`H`); the status "bounded accuracies with a field: open" of §11.20 is unchanged.

**(d) Site-dependent slopes.**
*Lemma N14 (sorted-slope Harper bound) [proved here; against all subsets for `m ≤ 4`: §7.1 C].*  On `Q_m` with the
uniform measure and the envelope `ρ(x,y) = Σ_iu_i[x_i ≠ y_i]`, let `U_j` be the sum of the `j` largest slopes.  If
`|{V > s}| ≤ |B(m,r)|`, `r ≤ m−1`, then `E(V − s)₊ ≤ s·2^{−m}Σ_{j=1}^{r+1}(e^{U_j} − e^{U_{j−1}})·|B(m, r+1−j)|`.  Proof: a
point at Hamming distance `k` from `Dᶜ` has `ρ(x→Dᶜ) ≤ U_k`; the sets `{dist ≥ j}` are bounded by Harper as in Lemma
11.43(b).  ∎  It is exact when all slopes are equal and loses otherwise (exact/bound down to `0.007` on `Q_4`).  At
the exponential scale it is the profile of the cube with the slopes sorted in decreasing order along the depth:
for two kinds in equal parts the hinted exponent it yields is that of the homogeneous cube with the *larger* slope
(`0.0974` against the true `0.0525` for slopes `(2, 0.5)`; §7.5 P6).  **Valid for every `n`, explicit, not sharp.**
*Proposition N19 (a continuum of slopes) [proved here, given Theorem 11.101 [P by transfer, reviewed]].*  Binary
sites, uniform measure, slopes `u_i ∈ [0, u_max]` whose empirical law converges weakly to `ν`.  Then for
`0 < ε₁ < E_ν` the adaptive and non-adaptive exponents are those of the game function
`J_ν(t) = ∫[Λ(tu) − tΛ(u)]ν(du)`.  Proof: round the slopes up, resp. down, to a grid of mesh `ε` whose points are
not atoms of `ν`.  The `o(n)` sites in cells of vanishing mass are enumerated for the upper bound (the mean over
their `2^{o(n)}` configurations of problems on the other sites, whose fibres stay in the class: a factor `e^{o(n)}`
in the cost) and given the slope `0` for the lower bound.  Enlarging the class gives an upper bound, shrinking it
a lower bound, each by Theorem 11.101 for finitely many types of positive fractions; the two game functions
differ by `O(ε)` uniformly in `t` because `u ↦ Λ(tu) − tΛ(u)` is Lipschitz on `[0, u_max]`.  ∎

**(e) Continuous site spaces of bounded diameter with the sum metric** (`X = ΠX_i`, `d = Σd_i`, `μ = ⊗μ_i`,
`diam(X_i, d_i) ≤ Δ_i`, slopes included in `d_i`; the class is `−ln V ∈ Lip₁(d)`).
*Lemma N15 (ball-volume tail function) [proved here].*  In any metric probability space let
`β(r) = inf_xμ(B°(x,r))` and `r_in(q) = sup{r : β(r) ≤ q}`.  Then `Ξ_in(q) = q·(e^{r_in(q)} − 1)` is an upper tail
function of `Lip₁`: a point of `D = {V > s}` at distance `r` from `Dᶜ` has `B°(x,r) ⊆ D`, so `r ≤ r_in(μ(D))`.  ∎
*Lemma N16 (transport tail function) [proved here; McDiarmid's bounded-differences inequality with the constant
`2` quoted from memory, to be verified (McDiarmid 1989)].*  With `σ² = ΣΔ_i²`, `R = ΣΔ_i`,
`r₀(q) = σ√(ln(1/(1−q))/2)`:

    Ξ_T(q) = ∫₀^R e^r · min{ q, exp(−2(r − r₀(q))₊²/σ²) } dr

is an upper tail function.  Proof: `g = dist(·, Dᶜ)` is `1`-Lipschitz, vanishes on a set of measure `≥ 1 − q`, so
`Eg ≤ r₀(q)` and `μ(g ≥ r) ≤ e^{−2(r−r₀)²/σ²}`; also `μ(g > r) ≤ q`; integrate `e^r·μ(g > r)`.  ∎
*Is either sharp?  No — proved on the cube, where the truth is known* (§7.1 E, §7.5 P3, P4).  Exponents at `u = 1`:
true `h = 0.0291`, `ε* = 0.1201`; ball-volume `h = 0.197`, threshold `0.5`, and its non-adaptive exponent at
vanishing accuracy is `ln 2` (enumeration); transport: threshold `u²/8 = 0.125` (nearly right), `θ_hint,T(0) = u²/2 =
0.5`, vacuous against enumeration for `u ≥ 1.18`, and — the decisive defect — its relative tail `Ξ_T(q)/q ≥
e^{σ√(ln(1/q)/2)} − 1` *grows* as `q → 0` (up to the diameter): concentration bounds how deep a set of measure `q`
can be only through `√(ln(1/q))`, so with a threshold below `e^{σ√(ln(1/q_at)/2)}` — on the cube: at every accuracy
rate below `0.589u`, hence at every rate below `ε*` — Algorithm A does not close with it before the atom (and never,
without atoms).  **A transport or
infimum-convolution inequality gives a valid tail function and no usable closing level; what the method needs is
an isoperimetric statement for the erosion of small sets, which concentration does not contain.**  (The ball-volume
bound supplies a crude one: finite exponents, far from sharp.)
*Lemma N17 (discretisation) [proved here].*  Partition each `X_i` into cells of `d_i`-radius `≤ δ_i` around
representatives; let `π_i` be the cell masses and `d̃_i` the metric between representatives.  For `ψ ∈ Lip₁(d)` its
restriction `ψ̃` to the product of representatives is in `Lip₁(d̃)` and `|ln A(ψ) − ln Ã(ψ̃)| ≤ Σδ_i`.  So a bracket
procedure of accuracy `x` for the finite-alphabet problem `(⊗π_i, d̃)` is one of accuracy `x + 2Σδ_i` for the
continuous problem, with the same queries.  ∎  For `n` circles with slope `ū` and `k` arcs each, Theorem 11.101(b)
(whose site envelopes are arbitrary quasi-metrics) gives the adaptive upper bound
`exp(n·R̂^{(k)}(ε₁ − 2πū/k) + o(n))` for every `k`.  **Not proved:** convergence of `R̂^{(k)}` as `k → ∞`, and a matching
lower bound (a lower bound for the discretised class does not transfer: the continuous algorithm may query
between representatives).  *Exact isoperimetry* for the sum metric on the discrete torus `ℤ_k^n` is in the
literature for even `k` (Bollobás–Leader, "An isoperimetric inequality on the discrete torus", 1990) — **quoted
from memory, to be verified, not used here**; if it has the form "balls are extremal", a Harper-type exact tail
function follows for discretised circles as in Lemma 11.43(b).

**(e′) Gauss space with the sum metric — a continuous instance with exact tail functions** (new here).  Functions
on `ℝ^m` that are `c`-Lipschitz for `ℓ₁` are `c√m`-Lipschitz for the Euclidean norm, so `Ξ_{c√m}`, `Θ_{c√m}` of Theorem
N9 are tail functions; they are **attained** in the class — by `V = e^{c(Σx_i − t√m)₊}` and `e^{−c(Σx_i − t√m)₊}`,
whose logarithms are `c`-Lipschitz for `ℓ₁` — hence exact for every `m` (§7.4 G3: the diagonal half-plane gives
`0.9999`, a coordinate half-plane `0.63`).  The family is a scale family: fibres and fibre averages stay in the
class, `(1/m)ln[Ξ_{c√m}(e^{−mθ})/e^{−mθ}] → ((c − √(2θ))₊)²/2` uniformly ((U) by the inequality of §5.1), the space is
atomless and unbounded with `E e^{c|x|₁} = (2e^{c²/2}Φ(c))^m < ∞`, so Theorem N1′ applies with
`ln(u₀/ℓ₀) = m·ln(Φ(c)/Φ(−c))`, and the profile `w(θ) = c²/2 − c√(2θ)` (`θ ≤ c²/2`), `−θ` beyond, satisfies (P0)–(P2).
By Proposition N6: **adaptive algorithms cost at most `exp(n·(c²/2 − ξ)²/(2c²) + o(n))` at the accuracy `ξn`**, the
base family `exp(n·(c/√2 − √ξ)² + o(n))` — in units of `c²/2` the "Gaussian pair" `(1 − √x)²`, `(1 − e)²/4` of the
report, here not as a small-slope limit but exactly, and with extensivity (a block of `φm` coordinates has the
profile `φw(θ/φ)`).  **Open:** lower bounds.  The extremal dips are half-spaces with normals in `{±1}^m/√m`; two
evaluations at `±Re₁`, `R` large, exclude all of them, so the hinted bound does not follow from them, and bounded
alternatives (dips on `ℓ₁`-balls, or half-spaces cut by a box) seem to give only weaker exponents (a box of side
`√(2 ln n)` loses a factor `ln n` in the exponent) **[heuristic]**.

**(f) A nearest-neighbour chain as known part.**  Outer block: sites `1..c`, law `μ_o` = the chain's marginal;
inner block: the rest under `μ(·|a)`, which depends on `a_c` only.  (F1′) asks the inner procedures to work for a
chain with a boundary field — the same kind of problem.  (F2′): the class-relative influence of the boundary
letter is the report's one-sided slack (Theorem 11.116(d), there "a bound on the game function, not a reduction of
algorithms"): with `g(v) = ln[((1−p)e^v + p)/(pe^v + 1−p)]` for the symmetric binary chain, `v^{(1)} = u`,
`v^{(j+1)} = u + g(v^{(j)})`, the function `−ln V` is `u`-Lipschitz in every outer letter but the last and
`(u + g(v^{(k)}))`-Lipschitz in the last, `k` the inner length — below `u* = u + g(u*) < u + K`, and attained by the
uniform field.  §7.3 S6 (`c = 4`, `k = 6`): observed `1.525944`, `2.740225`, `1.128162`, equal to `u + g(v^{(6)})` to
seven digits, against `u + K = 1.847`, `3.197`, `1.886`; with the envelope *without* the slack (TU) is violated (by
factors up to `5.7`), with it Algorithm A is valid in 360 of 360 runs (exact tail functions of the chain marginal
by enumeration).  **So Theorem N4 turns the one-sided slack into a statement about an algorithm: nesting is valid
on a chain without cutting it, with slack at one site per level** [proved here].  What is missing is cost: a tail
profile for a Markov measure with this envelope.  Lemma N18(a) transfers one from the product of free blocks of
length `ℓ` (`c₁ = c₂ = (m/ℓ)ln(1/2p)` for the symmetric chain), which gives the profile of *plain sampling from the
block product* up to `O(1/ℓ)` — the worse exponents of dead end D47, not `R̂`; the right sampler for a chain is not
known (the report: "the Rényi centre is not a Markov chain").  The abstract theorem gives nothing beyond Theorem
11.116(f) at the exponent level, and says where the gap is.

---

## 5. N5 — obstructions

### 5.1 Gauss space with Euclidean-Lipschitz functions: coordinate nesting gains nothing

**Theorem N9 (exact tail functions on Gauss space) [proved here, given the Gaussian isoperimetric inequality
`γ_n(A + rB₂) ≥ Φ(Φ^{−1}(γ_n(A)) + r)` — Sudakov–Tsirel'son 1974, Borell 1975; quoted from memory, to be verified
against the sources; closed forms against quadrature to `10⁻¹³`, the inequalities on Lipschitz functions in
dimensions `1`, `2` and for radial functions in dimensions `3` to `200`: §7.4 G1, G2].**  Let `n ≥ 1`, `L > 0`, and
`V : ℝⁿ → (0, ∞)` with `−ln V` `L`-Lipschitz for the Euclidean norm.  Then under `γ_n`, with `t = Φ^{−1}(1−q)` and
`c = Φ^{−1}(p)`,

    Ξ_L(q) = ∫₀^∞ Le^{Lr}Φ(−t−r) dr = e^{L²/2 − Lt}Φ(L − t) − Φ(−t),        Θ_L(p) = ∫₀^∞ Le^{−Lr}Φ(c+r) dr = p + e^{Lc + L²/2}Φ(−c − L)

are tail functions of `V`, attained by `e^{L(x₁−t)₊}` and `e^{−L(x₁−c)₊}`: they are the exact tail functions of the
class, **the same in every dimension**.
*Proof.*  Lemma N.0 with `ρ = L|x − z|`: `∫_D(e^{L·dist(x,Dᶜ)} − 1)dγ = ∫₀^∞Le^{Lr}γ{dist(·,Dᶜ) > r}dr`;
`{dist(·,Dᶜ) > r}` is the complement of `Dᶜ + rB₂`, and `γ(Dᶜ + rB₂) ≥ Φ(t + r)` because `γ(Dᶜ) ≥ Φ(t)`.  Likewise
`∫e^{−L·dist(x,S)}dγ = ∫₀^∞Le^{−Lr}γ(S + rB₂)dr ≥ ∫₀^∞Le^{−Lr}Φ(c + r)dr`.  The closed forms: integrate by parts and
complete the square.  ∎
*Profile.*  For `t ≥ 0`: `1 + Ξ_L(q)/q ≤ 3(1+t)·e^{(L−t)₊²/2}` (from `Φ(−t) ≥ e^{−t²/2}/(3(1+t))` and
`Φ(−x) ≤ ½e^{−x²/2}`; §7.4 G1), and `1 + Ξ_L(q)/q ≥ e^{(L−t)²/2}` on `0 ≤ t ≤ L` (from `Φ(L−t) ≥ ½`,
`Φ(−t) ≤ ½e^{−t²/2}`).  With `q = e^{−Θ}` and `L → ∞`:
`ln Ξ_L = L²/2 − L√(2Θ) + O(ln L)` for `Θ ≤ L²/2` and `−Θ + O(ln L)` beyond; so `Θ_hint(e) = (L/2 − e/L)²/2`,
`Θ_na(X) = (L − √(2X))₊²/2` — in units of `L²/2` the Gaussian pair, as the brief computed.  The scale is `L²/2`, not
`n`: (F1), (F2) hold for every split `ℝⁿ = ℝ^{n_o} × ℝ^{n_i}`, **but there is no trivial bracket** (`V` is unbounded):
Algorithm 2L⁺ as stated does not apply, Theorem N1′ does (`ln(u₀/ℓ₀) = ln[E e^{L|x|}/E e^{−L|x|}] ≈ 2L√n`).  At a
bounded threshold `θ` the two-sided condition [P] holds from `t = L + O(√(ln(1/θ)))` on (for `t > L`:
`Ξ_L ≈ q·L/(t−L)` against `Θ_L ≥ ½e^{L²/2−Lt}`) **[sketch]**; in §7.4 G5 the closing levels at `θ = ½` are
`π_* = 0.039` and `0.0013` for `L = 1.5`, `2.5`, i.e. `t − L = 0.26`, `0.52` — the analogue of the `O(√m)` of Lemma 11.55.

**Proposition N10 (nesting over a fixed split of the coordinates gains nothing) [proved here].**
(a) *The level operator.*  Because `Ξ_L` does not depend on the dimension, the exponent of a level with total
accuracy `G`, tolerance `B` and an inner family with exponent function `T` (all in total units, scale `L²/2`; the
computation of Corollary N5) is `sup_{γ≥B}[min(γ, Θ_na(G − B)) + T(γ)]`, without factors `φ`, `1 − φ`, and

    R_G[T](G)  :=  inf_{0<B<G} sup_{γ≥B} [ min(γ, Θ_na(G − B)) + T(γ) ]   ≥   max{ Θ_na(G) , T(G − 0) }

for **every** nonincreasing `T ≥ 0` (let `γ → ∞`; take `γ = B`).  So `min(T, R_G[T]) = T`: the recursion is the
identity, at `T = Θ_na` and everywhere else.  (For the Gaussian pair in units of `a`: two levels reach `0.5000` with
the factors `φ`, `1−φ`, and `0.98 ≥ θ_na = 0.74` without, at `G = 0.02a`; §7.4 G6.)
(b) *The algorithm, not only its bound.*  Let `x_out < L²/2` and consider the instance `ψ(a,b) = −L⟨a, ω⟩`, `ω` a
unit vector of the outer block with `⟨a₀, ω⟩ ≤ 0` at the reference point (linear, gradient in the outer block; in
coordinates `V(a) = e^{La₁}`, `A = e^{L²/2}`; the reference data of Theorem N3 give `ℓ₀ = e^{−ψ(x₀)}E e^{−L|x−x₀|} ≤ 1`,
and all that is used is `ℓ₀ < e^{−x_out}A`).  For
every `n_o ≥ 1`, `n_i ≥ 0`, any tail functions, any inner procedures and any parameters, every run of Algorithm A on
its good event has

    M_max  ≥  (2K/(1+η)) · exp( (L − √(2x_out))² / 2 ).

*Proof.*  (R7): `E min(V, e^{Lt}) = A·[Φ(t − L) + e^{Lt − L²/2}Φ(−t)] ≤ A·e^{−(L−t)²/2}` for `0 ≤ t ≤ L`, and
`ℓ₀ ≤ 1 < e^{−x_out}A`; so `t_x ≥ L − √(2x_out)` in the variable `t`, and
`p(e^{Lt}) = Φ(−t) ≤ ½e^{−t²/2}`.  ∎  (Six runs with `x_out < L²/2` in §7.4 G5: the bound holds with a factor `560` to
spare — it is a bound, not the cost.)  The base family already costs `e^{Θ_na(x)}·poly` on the whole class
(Proposition N2 with Theorem N9).  So with a fixed split the worst case of a level is never below the base
family's: the outer problem is a full copy of the original one, at any dimension.  On the cube the same lemma gives
`e^{n_oθ_na(x/n_o)}`, which *is* smaller for a smaller block — entry 30 of the audit.

**Proposition N11 (the hinted lower bound holds in high dimension — with balls, not half-spaces) [proved here,
given the cap bound `σ_{n−1}(ω₁ ≥ s) ≤ e^{−ns²/2}` (Ball 1997, Lemma 2.2; quoted from memory, checked numerically for
`n ≤ 3000`) and the median of `χ²_k` being below `k` (checked for `k ≤ 10⁶`); the dip's effect by quadrature for
eleven triples `(L, t, n)`: §7.4 G4].**  Let `0 < t ≤ L`, `T = L + 1.2816`, `n ≥ max{4t², L·T²·t}`, and
`0 < ε < ln(1 + 0.112·e^{L²/2 − Lt} − ½Φ(−t))`.  Every randomised algorithm on `(ℝⁿ, γ_n, Lip_L)` that is
`(ε/2, δ)`-correct — adaptive, with any hint — makes at least `(1 − 2δ)·e^{t²/2}` evaluations in expectation at
`ψ ≡ 0`.  In exponents (`t = L/2 − (ε + 2.2)/L`, `ε ≥ 1`): about `Θ_hint(ε + 2.2)`.
*Proof.*  Alternatives: for a unit vector `ω`, the dip `g_ω(x) = −L(ρ − |x − r₀ω|)₊` with `r₀ = n/t`,
`ρ² = n²/t² − n`; it is `L`-Lipschitz and differs from `0` exactly on the ball `B(r₀ω, ρ)`.  *Hit fraction:* a point
`x` with `|x| = r > 0` lies in that ball iff `⟨x/r, ω⟩ > (r² + n)/(2rr₀) ≥ √n/r₀ = t/√n`, so for `ω` uniform on the
sphere the probability is at most `e^{−t²/2}` (and `0 ∉` any ball).  *Effect:* with `y = 2r₀(x₁ − t) − (|x|² − n)`,
`|x − r₀e₁| = √(ρ² − y) ≤ ρ − y/(2ρ)`; on the event `{|x_⊥|² ≤ n−1}` (probability `≥ ½`, independent of `x₁`) and for
`t < x₁ ≤ T` the depth is at least `(x₁ − t) − T²/(2ρ)`, and `LT²/(2ρ) ≤ 0.578` under the hypotheses; hence
`A(g_ω) − 1 ≥ ½[e^{−0.578}e^{L²/2−Lt}(Φ(T−L) − Φ(t−L)) − Φ(−t)] ≥ 0.112e^{L²/2−Lt} − ½Φ(−t)`.  *Averaging* (the argument
of Theorem 11.22(c), which is Fubini and holds for a probability measure on alternatives): couple the runs on `0`
and on `g_ω` with the same random bits; they coincide unless a query falls into the ball, and no output is correct
for both, so each ball is hit with probability `≥ 1 − 2δ`; integrate over `ω`.  ∎
Numerically the ball dip has `0.94` to `0.9999` of the half-space's effect for `n` between `100` and `10⁵` (G4).

**What is and is not shown about adaptive algorithms on Euclidean Gauss space.**  Shown: the exponent lies between
`Θ_hint(ε + O(1))` (Proposition N11, for `n ≥ L(L+1.29)²t`) and `Θ_na(ε)` (base family, every `n`) — the situation
of the cube before Theorem 11.54; and nesting over a fixed coordinate split cannot close the gap.  Not shown, and
**open:** whether any adaptive algorithm goes below `Θ_na`.  Not excluded by Proposition N10: *random* blocks.  For
a random subspace of dimension `φn` a linear function has outer slope `≈ L√φ` and inner slope `≈ L√(1−φ)` — the
Lipschitz budget `L²` splits like the dimension, as the sum metric does — but for a general member the split of
`|∇ψ|²` varies from point to point and (F2) holds only with the constant `L`; a theorem would need tail functions
for functions that are `L√φ`-Lipschitz outside an exceptional set **[heuristic; open]**.  In low dimension
(`n ≪ L²/ln L`) grids beat all of this and the exponents in units of `L²/2` are not the right scale.

### 5.2 Unbounded influence: (F2) fails, and the algorithm certifies a false bound

**Proposition N12 [(a)–(c) proved here; (d) numerical].**  Let `X_o = Q_m` with the uniform marginal,
`X_i = Q_k`, `μ(·|a) = Bernoulli(p(a))^{⊗k}` with `p(a) = σ(J(τ − |a|))`, `τ` a half-integer — the Gibbs measure
of a complete bipartite coupling of strength `J` per pair (not divided by `n`) with a field, corrected by a
function of `|a|` so that the outer marginal is uniform — and the residual `ψ(a,b) = u|b|`.
(a) `ψ ∈ L_u(Q_{m+k})` is additive and does not depend on `a`; (F1) holds.
(b) `V(a) = (1 − p(a) + p(a)e^{−u})^k`, and across the threshold
`ln[V(a′)/V(a)] = k·ln[(1 − σ(−J/2)(1−e^{−u}))/(1 − σ(J/2)(1−e^{−u}))] =: k·c(J,u)`, `c(J,u) ↑ u` as `J → ∞`.  So `−ln V`
is Lipschitz on the outer cube with no constant below `k·c`: **(F2) fails by the factor `e^{kc − u}`, which grows
exponentially with the size of the inner block.**  The pointwise influence is of order `kJ` per outer flip
(`kJ/2` at the threshold, `kJ` away from it), the class-relative one `k·c(J,u)`: both unbounded.
(c) With `D = {|a| > τ}` and `s` the largest value of `V` outside `D`: `E(V − s)₊ ≥ s·μ_o(D)(e^{kc} − 1)`, while
Harper's function for the assumed class gives `s·Ξ_u(μ_o(D)) ≤ s·μ_o(D)(e^{u(m−τ+½)} − 1)`: (TU) is violated as soon
as `kc > u(m − τ + ½)`.
(d) *What the algorithm does* (§7.3 S4: `m = 12`, `k = 16`, `u = 1`, `J = 4`, `τ = 10.5`; `A = 1.07·10⁻³`, of which
the 13 points with `|a| ≥ 11` carry `100.0 %`; the bulk has `V ≤ 1.2·10⁻⁷`; largest edge ratio `e^{11.77}`; (TU) for
the slope `u` fails by `1.7·10⁵`).  Run with the tail function of the assumed class it stops after a median of
`1 164` (resp. `6 816`) outer points and **returns an invalid bracket in 80 of 80 runs — the certified upper end is
below `A` by a median factor `294` (`θ = 20`) and `3 680` (`θ = 1`)**; the Chernoff events held in all 80, so this is
not a sampling accident: every certificate obtained by sampling stays true, the false step is the tail bound, and
the run closes below the spike.  Run with the tail function of the true class of `V` (slope `11.77`) it is valid in
80 of 80 runs and draws a median of `1.0·10⁵` (resp. `9.2·10⁵`) outer points — `25` to `225` times the `4096` points
of the outer cube: a cost blow-up to (more than) an enumeration, as the closing level falls to the atom.
*Mechanism* (general): the run is invalid iff it closes at a level below the spike, which happens when the spike
is higher above the bulk than the reciprocal of the closing level (times `ν₀`) and carries more than `e^{x_out}`
times the bulk mass.  *Not a counterexample:* unbounded influence confined to boundedly many outer sites (a hub):
condition on them (`2^{k₀}` sub-problems); the failure needs the influence to be spread, as here.

### 5.3 Unbounded oscillation: what is needed instead of a trivial bracket

**Proposition N13 [proved here].**  Let `𝒞 = {ψ : ψ(z) − ψ(x) ≤ d(z,x)}` on `(X, μ)`, `d` a quasi-metric.
(a) *An exponential moment is necessary and sufficient for any certified upper bound.*  `sup{A(ψ) : ψ ∈ 𝒞,
ψ(x₀) = ψ₀} = e^{−ψ₀}∫e^{d(x₀,x)}μ(dx)`, attained by `ψ = ψ₀ − d(x₀,·)`.  If this integral is infinite for one `x₀` it
is infinite for all, and after any finite set of evaluations the instances consistent with them have unbounded
`A` (the upper McShane envelope `min_ie^{−ψ(x_i)+d(x_i,x)}` dominates a positive multiple of `e^{d(x₀,x)}`): no
algorithm can return a finite upper bound.  If it is finite, one evaluation gives
`e^{−ψ₀}∫e^{−d(x,x₀)}dμ ≤ A ≤ e^{−ψ₀}∫e^{d(x₀,x)}dμ`; the lower bound needs no moment.
(b) *What the level theorem needs instead of a cap.*  (i) the bracket `ℓ₀ ≤ A ≤ u₀` of (a); (ii) for every fibre
the same under the inner law (rung `0`); (iii) a tail function with a closing level `π_* > 0`: then Theorem N1′
holds, the termination coming from the closing level.  A cap on `V` is needed for nothing; it is available without
any moment condition if the class is restricted to functions bounded below on the outer block.
(c) *Without (iii)* — an atomless outer law and a tail function whose ratio `Ξ(q)/q` does not stay below the
threshold as `q → 0` — the algorithm has no bound on its sample: every negligible level is left with a failed test
and the ladder has no top.
Gauss space satisfies (i)–(iii) for both metrics (`Ξ_L(q)/q → 0`); §7.4 G5: 105 runs of the unbounded variant on
`ℝ³ … ℝ⁶`, all closed, all valid, none above level `J`.

---

## 6. N6 — the assumption table of Theorems 11.52 / 11.56 / 11.54 / 11.58

Categories of the directive: **E** essential; **P** required only by the present proof technique; **C** introduced
for convenience; **W** replaceable by a weaker quantitative condition (stated); **X** removal changes the
complexity (how); **F** removal makes the result false (counterexample).  "Thm" = which theorems carry the
assumption (52, 56 = the level theorems; 54, 58 = the exponents).  Evidence: a statement of this report, of the
theory report (with its label), or "not known".

| # | assumption | Thm | category | what holds without it; evidence |
|---|---|---|---|---|
| 1 | the two blocks are independent (product measure) | 52, 56 | **W**, then **F** | W: class-relative influence `ι`: (F2) with the envelope `d_o + ι` (Theorem N4, proved here; S3, S6).  F: unbounded influence — (TU) fails by `1.7·10⁵`, 80/80 invalid brackets (Proposition N12) |
| 2 | (F2): `−ln` of fibre averages is in a class with a known tail function; in particular the slope `u` is known | 52, 56 | **E**, **F** | the only step whose failure makes the bracket false; same counterexample (assumed slope `1`, true `11.8`); a mutation test with `Ξ/50`: 4 of 48 runs invalid (§7.3 M) |
| 3 | (F1): fibres are in a class with inner procedures | 52, 56 | **E** for the method, **P** for the exponent | the radial class of Theorem 11.51 is not closed under fibres and has the exponent `θ_hint` by another algorithm [quoted, P] |
| 4 | uniform reference measure | all | **W**, **X** | W: any product measure with a reference instance (Lemma 11.62, Theorem 11.64 [P]; Lemma N18(b)).  X: exponents become `R^max ≤` uniform — "a field always helps" (Proposition 11.65(b) [P]).  At bounded accuracy (56, 58): **not known** (needs a two-sided tail estimate, §4(b)) |
| 5 | binary alphabet | all | **W**, **X** | any finite alphabets, site types, asymmetric envelopes: Theorem 11.101 [P by transfer]; exponents are Rényi capacities (Theorem 11.99).  Bounded accuracy: **not known** |
| 6 | one slope for all sites | all | **W** | site types (Theorem 11.101); a continuum of slopes: `J = ∫J_u dν` (Proposition N19); explicit non-sharp tail function for every `n` (Lemma N14) |
| 7 | the metric is a sum over sites (a block of `φn` sites has the profile `φw(·/φ)`) | 52 (cost), 54, 58 | **P**, **X** for the algorithm | without it the level operator is the identity and the outer sample of every level costs `e^{Θ_na}` (Proposition N10, proved here: Euclidean Gauss space).  Whether the *complexity* changes: **not known** (between `Θ_hint` and `Θ_na`; Proposition N11) |
| 8 | exact isoperimetry (Harper) for the upper tail | 52, 56 | **W**, **X** | W: validity with any upper tail function; the exponent with one that is sharp at the exponential scale, uniformly over smaller sets (condition (U)).  X: a non-sharp one changes the cost — ball-volume: `h = 0.197` for `0.029`; transport: closing only at the atom (§4(e), proved) |
| 9 | the lower tail lemma (Harper term) | 56, 58 | **W** | `Θ = id` is always valid and gives Theorem 11.52 (extensive accuracies); bounded accuracy needs `Ξ(q) ≤ θ·Θ(c_ηq)` down to `q = e^{−m(a+o(1))}` — available for the uniform cube (Lemma 11.55) and, from the explicit formulas, for Gauss space (closing at `t = L + O(1)`, §5.1; no analogue of Lemma 11.55 is written out), **not known** elsewhere |
| 10 | bounded oscillation (finite diameter) | all | **W**, **F** | W: a lower bound `ℓ₀`, an exponential moment for the inner block, and a cap on `V` *or* a closing level `π_* > 0` (Theorems N1, N1′).  F: without the exponential moment `A` can be infinite and no finite upper bound is certifiable (Proposition N13(a)) |
| 11 | atoms; a finite space | 52, 56 | **C** | not used (Theorem N1); the enumeration fallback of the families is replaced by the base family (Proposition N2) |
| 12 | integrality of radii (ball sizes) | 52, 56 | **C** | `Ξ` is evaluated at `q`; segments of the simplicial order give the exact function at every size (§2.5 R3) |
| 13 | the ladder starts below the integrand (`s₀ ≤ min W`) | 52, 56 | **C** | any `s₀ = κ₀ℓ₀`, `κ₀ ≤ 1` (S2 of §7.3 with `κ₀ = 1` and `0.02`) |
| 14 | `J = ⌈(2un + b + n_o ln 2)/λ⌉` | 56 | **C** | `⌈2un/λ⌉` with rule (c0) |
| 15 | cost bounds of inner procedures hold in every run | 52, 56 | **C** | makes the abort rule possible; a bound on the good event only would give a cost bound of the same kind (not written out) |
| 16 | thresholds fixed by the reference query (a geometric ladder, non-adaptive in the levels) | 52, 56 | **P** | Chernoff at fixed thresholds; whether adaptive thresholds save the factor `J`: **not known** |
| 17 | extensive accuracy | 52, 54 | **P** | removed on the uniform cube by Theorems 11.56, 11.58; elsewhere open (rows 4, 5, 9) |
| 18 | accuracy with `ln(1/ε_n) = o(n)` | 58 | **X** | for `ε = e^{−cn}` the hinted bound of Theorem 11.25(a) counts balls with `2^{−n}E_k ≈ e^{−cn}`: a larger exponent (`θ_hint` at a negative rate); the upper bound there was not examined here — **partly known** |
| 19 | randomisation | all | **E**, **X** | deterministic algorithms cost `≈ 2ⁿ` on the cube class [quoted: `cube_deterministic_lower_bound`, V; theory report, table row G11] |
| 20 | adaptivity | 54, 58 | **E**, **X** | non-adaptive exponent `θ_na > θ_hint` (Theorem 11.45 [(a) V, rest P]) |
| 21 | failure probability `δ < ½` (lower bound); `δ ≥ e^{−cn}` (upper bound) | 54, 58 | **E** (lower), **P** (upper) | the factor `1 − 2δ`; smaller `δ` than `e^{−O(n)}`: **not known** |
| 22 | worst case over the class | 54, 58 | **E** | instance by instance the nested algorithm is not shown to match the hinted cost (remark (4) after Theorem 11.54: open); (R7) gives the instance-wise cost of its outer sample |
| 23 | exact evaluations (no noise) | all | — | **not known**; not examined anywhere in §11.18–11.19 |
| 24 | transitivity of the cube (every query point is typical), in the lower bound 11.25(a) | 54, 58 | **P** | generalised dips with vertex labels give lower bounds without it (Theorems 11.59(a), 11.101(a), 11.116(c) [V/P]); on Gauss space half-space dips fail and ball dips work for `n ≥ L(L+1.29)²t` (Proposition N11) |
| 25 | a fixed split into coordinate blocks | 52, 56 | **C** on the cube, **P** elsewhere | on the cube any split of the sites is equivalent; heterogeneous sites: the best split is not proportional (§3.2, numerical); Gauss space: random subspaces not covered by the obstruction (§5.1, open) |

**Counts** (an entry with two labels counts twice): **E 6** (rows 2, 3, 19, 20, 21, 22); **P 7** (3, 7, 16, 17, 21,
24, 25); **C 6** (11, 12, 13, 14, 15, 25); **W 7** (1, 4, 5, 6, 8, 9, 10); **X 7** (4, 5, 7, 8, 18, 19, 20); **F 3**
(1, 2, 10); row 23 has no label.  "Not known" appears in rows 4, 5, 7, 9, 16, 21, 23 (and in part in 18).

**The three most consequential entries.**
(1) *Row 7, the sum metric.*  It is "cost only" in the proof and it is the whole gain: the same theorem, with the
same hypotheses verified, yields nothing on Euclidean Gauss space.  A hierarchy of instances should be organised by
whether the envelope is additive over independent parts — not by whether the space is discrete or continuous
(Gauss space with the sum metric is an instance, with exact tail functions).
(2) *Rows 1–2, (F2).*  The one hypothesis whose failure produces a *false certificate* rather than a higher cost.
The right quantitative form is the class-relative influence `ι`; with it dependence costs slope (`u → u + ι`), and
unbounded influence costs validity.  A certificate format built on this theorem must carry the bound on `ι`.
(3) *Rows 8–9, the isoperimetric input.*  Exact isoperimetry is not needed for validity and not for the exponent,
but concentration is not enough: the method needs a bound on the tail of *small* sets relative to their measure,
uniformly, and at a bounded accuracy a two-sided one with polynomial precision.  That exists for the uniform cube
and Gauss space only; for every other instance of the report the bounded-accuracy theory (Theorem 11.58) is open
for this reason and no other.

---

## 7. Numerical checks

All in `experiments/workstreams/N/` (numpy, scipy; one process, below 1 GB; run from that directory).  Every script
exits with status `0` iff it found no violation.  `nlib.py` is the shared library (`python3 nlib.py`: self-test).

### 7.1 `python3 n1_tail_bruteforce.py > out_n1_tail_bruteforce.txt` (9 s) — tail functions on small cubes
A. `Q_m`, `m = 2, 3, 4`, `u ∈ {½, 1, 2}`, all subsets (65 534 for `m = 4`): the exact upper and lower tail functions
equal Harper's `E_r`, `T_k` at ball sizes, are `≤` (resp. `≥`) Harper's step functions elsewhere, and are attained by
segments of the simplicial order at every cardinality — 9 of 9 cases.  B. (TU), (TL) with Harper's functions on
random members of `L_u(Q_m)` of five kinds, `m = 6, 9, 12`: 695 283 levels, largest ratio `1.0000`, no violation.
C. Lemma N14 on `Q_3`, `Q_4` with four slope patterns: valid; exact/bound between `0.007` and `1`.  D. A biased
product measure on `Q_4`: the enumerated functions satisfy (TU), (TL) on 400 random members.  E. Ball-volume and
transport bounds against Harper on `Q_m`, `m ≤ 256`: valid; Harper/transport between `0.44` and `10⁻⁶⁶`.

### 7.2 `python3 n2_cube_constants.py > out_n2_cube_constants.txt` (1 s) — the cube as a special case
Ten parameter sets (`u ∈ {½, 1, 2}`, `n ≤ 600`, bounded and extensive thresholds, `r† = −1` included).  With the
cube's conventions, `J`, `ν₀`, `r†`, `ln π†`, `m_max`, `K`, `ln M̄`, `ln δ′`, `x_out`, `ln C_max` of Theorem N1 — the
closing level computed from the abstract conditions in `q` — against `qlib.level_consts`/`level_cmax` (workstream
Q's evaluator of Theorem 11.56): **all equal in 10 of 10**.  With the abstract conventions: `J` smaller (e.g. `2000`
for `2350`), `ln C_max` smaller by `0.004 … 0.29`, `x_out` identical.

### 7.3 `python3 n3_sim_abstract.py > out_n3_sim_abstract.txt` (2 min) — Algorithm A on exact instances
The outer loop is run literally; the inner procedures are an oracle that returns valid brackets of the promised
ratio around the exact `V(a)` (random, top, bottom, adversarial placement), so (V1) holds by construction; (V2), (V3)
are verified on the realised sample; `check_run` tests validity, width, certificates, closing level, sample sizes,
the count, the calls and termination.  **Not end to end:** no real inner bracket procedure is run (for the cube
that is `K_REPORT.md` §6.5).

| scenario | runs | result |
|---|---|---|
| S1 cube `Q_{n_o} × Q_{n_i}` (`n_o ≤ 10`), exact fibre averages of random `ψ`, three parameter regimes, abstract and cube conventions | 1 296 | all valid; no check failed; 70 208 populated levels |
| S1b radial outer landscapes, `ν₁ = 1`, small `θ` | 192 | all valid; **163 levels left as negligible**; largest sample `3.3·10⁶` |
| S2 `Q_4`, biased measure, weighted envelope, enumerated tail functions, `κ₀ ∈ {1, 0.02}` | 576 | all valid; 24 stops by rule (c0) |
| S3 dependence, bounded influence (Theorem N4) | 120 | all valid; slope of `−ln V` = `u + kι₁` |
| S4 unbounded influence: (i) assumed class | 80 | **80 invalid** (Proposition N12) |
| S4 (ii) true class | 80 | all valid; samples `25–225 ×` the outer cube |
| S6 chain, one-sided slack, enumerated tail functions | 360 | all valid; slack attained to 7 digits |
| lowered cap (R6) in S1, S1b | 1 488 | largest sample / cap `= 0.607` |
| lower bound (R7) in S1–S3, S6 | 1 458 | smallest `M_max`/bound `= 3.5` |
| mutations: `q` without `1/(1−η)`; `Ξ/50`; none | 48 each | 20 certificate failures; 4 invalid brackets; 0 |

The good event held in all 2 624 runs of the valid settings (the union bound is very conservative at these sizes).
Thresholds are compared with a relative tolerance of `10⁻⁹`: a flat fibre puts the reference weight exactly on the
level grid — the structural tie of `K_REPORT.md`, errata (m10), (e2) — and without the tolerance the certificate
check failed on flat instances by floating-point rounding (found while writing the harness).

### 7.4 `python3 n4_gauss.py > out_n4_gauss.txt` (50 s) — Gauss space
G1 closed forms against quadrature (28 pairs, `9·10⁻¹⁴`); three elementary inequalities on grids.  G2 (TU), (TL) by
quadrature: `n = 1` (180 random functions × 50 levels: largest ratio `0.959`; half-lines `1.0000`), `n = 2` (grid
`2001²`: `1.0003`; a half-plane `1.0000`), radial functions for `n = 3, 20, 200` (`≤ 0.946`).  G3 the sum metric,
`m = 2`: random `ℓ₁`-Lipschitz functions `≤ 1.0001`; the diagonal half-plane `0.9999`; a coordinate half-plane
`0.63`, `0.36`.  G4 ball dips: effect / half-space effect between `0.938` and `1.009` (at `n = 30` the ball has
slightly more measure than the half-space; against the tail function at its own measure the ratio is `≤ 0.9999`),
the proved bound holds in the ten triples that satisfy its hypothesis; the cap bound.  G5 Algorithm A, unbounded
variant, on `ℝ³ … ℝ⁶` (Euclid `L ∈ {1.5, 2.5, 3.5}`, and `ℓ₁` with `c = 0.6`), five instances with exact `A`: 105 runs,
all closed, all valid, all within `J` levels; Proposition N10(b) in the six runs with `x_out < L²/2`.  G6 two levels
with and without extensivity.  G7 the base family on `ℝ⁶`: 2 000 brackets, all covering, all within the ratio
bound.
(An earlier version of the level check computed tail sums as differences of cumulative sums and reported false
violations by cancellation; the stored output is from the corrected routine, which sums from the top.)

### 7.5 `python3 n5_profiles.py > out_n5_profiles.txt` (45 s) — exponents
P1 the cube's profile from exact tables up to `m = 12 800` and the one-sided statement (U) on `q ≤ ½`.  P2
Proposition N7 for the cube at `u ∈ {½, 1, 2, 4}`: every `HintPair` field, `J(t) = Λ(tu) − tΛ(u)`, both dual formulas.
P3 the transport profile: (P1) fails, the identity fails.  P4 exponents of the non-sharp tail functions.  P5
heterogeneous families: Proposition N8 on 1 200 random splits; the two-level table of §3.2; the homogeneous value
`τ₂/a = 0.5004` reproduced.  P6 the sorted-slope bound at the exponential scale.

---

## 8. Errors and inaccuracies found

**In the brief (`N_brief.md` §2 — a sketch, as it says).**
1. §2(a)(iii), (vii): for Theorem 11.56 the list lacks the *lower* tail lemma (11.43(c), the Harper term).  At a
   bounded accuracy the cost is governed by the two-sided ratio `Ξ(q)/Θ(c_ηq)`; `Γ̃ = Ξ/q`, which the brief names, is
   never small on the cube (Lemma 11.55(a)) and closes only negligible levels.
2. §2(a)(v), (vi): `s₀ ≤ W` is not needed; "bounded oscillation" is three separate inputs (audit, (iii)); and atoms
   are not what bounds `M` in Theorem 11.56 (the closing level does) — they enter its termination argument and one
   convention, and are dispensable.
3. §2(b): the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` is not "by construction" for a general tail profile; it
   holds when `w(θ) + θ` is strictly decreasing where positive and can fail otherwise (Proposition N7; a
   counter-profile in §3.1).
   The convergence `(1/m)ln Ξ_m(e^{−mθ}) → w(θ)` must be one-sided *uniform over all smaller sets* and cannot hold up to
   `θ = 0`.
4. §2(c): "with `T = Θ_na` it is never below `Θ_na(G)`" is true and trivially so for every `T` (Proposition N10(a));
   the substantive statement is N10(b).  "(F1), (F2) hold" — but there is no trivial bracket on Gauss space, so the
   algorithm as stated does not apply (Theorem N1′ does).  The profile formula is for `Θ ≤ L²/2` (beyond: `−Θ`).
5. §2(d): the pointwise bound `ln[dμ(b|a)/dμ(b|a′)] ≤ L·d_o` is sufficient but not the sharp hypothesis (the
   class-relative `ι` is; the report's Theorem 11.116(d) has the sharp constant for chains); and "(F1) is unchanged"
   hides that the inner procedures must be valid under every conditional law.

**In the theory report.**
6. §11.18, remark (3) after Theorem 11.54: "Product reference measures and larger alphabets with a weighted Hamming
   distance have all three ingredients at the exponential scale (asymptotic isoperimetry of product measures; from
   memory, not read) and are not worked out."  Stale: §11.20 shows that this is the wrong object (dead end D47) and
   §§11.20, 11.26 work the cases out.
7. Same remark: on Gauss space "the extremal sets of the isoperimetric inequality are half-spaces, which an
   algorithm can detect with a few evaluations far from the bulk, so that even the hinted lower bound does not
   transfer."  The premise is right, the conclusion too pessimistic: dips on balls of radius `≈ n/t` with centres at
   distance `n/t` have the effect of the half-space up to a factor `1 − O(1/n)` (numerically: `0.992`, `0.9992`, `0.9999`
   at `n = 10², 10³, 10⁴` for `L = 3`, `t = 1`) and every point lies in a fraction `≤ e^{−t²/2}` of them, so the hinted
   lower bound holds for `n ≥ L(L+1.29)²t` (Proposition N11).  And "a block of coordinates has
   the same Euclidean Lipschitz constant as the whole space, so the two-level construction gains nothing as it
   stands" is now a proposition (N10), with the scope "fixed split".
8. `THY-MSG-0016` §3 item 1 lists Gauss space among the intended instances with "its pair is the Gaussian pair of
   the report".  With the Euclidean metric it is a documented failure of nesting; with the sum metric it is an
   instance, and the pair is exact (§4(e′)).
No error was found in the proofs of Theorem 11.52 (as corrected in the report) and Theorem 11.56/K1: every step
was re-derived for §2.4.  Two constants can be improved without changing anything else: `J` (row 14 of §6) and the
point bracket (`un_i` for `2un_i`).

---

## 9. What is not proved here; the weakest link

* **Proposition N6** rests on Proposition E of `K_REPORT.md`, whose proof I checked step by step for uses of the
  cube and did not rewrite; for the unbounded variant the same check (the level theorem enters only through
  Corollary N5) — **the weakest link.**
* **Theorem N1′** is new; its termination argument is five lines, and it has been run on Gaussian outer spaces of
  dimension `≤ 6` only, in runs where every level was populated.  The negligible branch of Algorithm A is exercised
  in the bounded variant (S1b), not in the unbounded one.
* Algorithm A is tested with a simulated inner oracle; **no end-to-end run with real inner procedures** exists
  outside the cube.
* Lower bounds are outside this workstream's theorems except Proposition N11.  In particular "`θ_hint = w^{−1}` is
  the adaptive exponent" is proved nowhere here; for Gauss space with the sum metric and for continuous sites no
  lower bound is known to me.
* The instances (b), (c), (f) are taken from the theory report with its labels (paper proofs by transfer, reviewed);
  nothing of them was re-derived here beyond the statements used.
* Literature quoted from memory: the Gaussian isoperimetric inequality (Sudakov–Tsirel'son; Borell), McDiarmid's
  inequality, the cap bound on the sphere, the median of `χ²`, Bollobás–Leader on the discrete torus (not used).
  The first is the only one on which a theorem of this report depends in an essential way.
* Open questions named above: adaptive algorithms on Euclidean Gauss space (random blocks?); bounded accuracy for
  every instance but the uniform cube and Gauss space; a tail profile for Markov measures with the one-sided slack;
  the level theorem for non-proportional splits and its effect on the rate; noise; instance-optimality.

**Three next steps, in order of expected value.**  (1) A two-sided tail estimate with polynomial precision for the
flat-histogram reference (the analogue of Lemma 11.55(b)): it would extend Theorem 11.58 to fields, alphabets and
site types in one stroke, through Theorem N1.  (2) Random-subspace nesting on Gauss space: either a tail function
for "Lipschitz outside an exceptional set" or an obstruction — it decides whether the sum metric is essential for
the complexity or only for this method.  (3) A lower bound for Gauss space with the sum metric (bounded
alternatives), which would make (e′) a complete continuous instance.

---

## Appendix: files

`docs/workstreams/N_REPORT.md` (this file).  In `experiments/workstreams/N/`: `nlib.py`; `n1_tail_bruteforce.py`,
`n2_cube_constants.py`, `n3_sim_abstract.py`, `n4_gauss.py`, `n5_profiles.py` with `out_n1_tail_bruteforce.txt`,
`out_n2_cube_constants.txt`, `out_n3_sim_abstract.txt`, `out_n4_gauss.txt`, `out_n5_profiles.txt`.  `n2` imports
`experiments/workstreams/Q/qlib.py` (read only).

## Summary (at most 45 lines)

1. **Abstract theorem (N2).**  Hypotheses: an outer integrand `V > 0` on a probability space `(X_o, μ_o)` with
   `A = ∫V dμ_o`; i.i.d. sampling; refinable brackets of `V(a)` with certified costs; an upper tail function `Ξ`
   (`μ_o(V > s) ≤ q ⟹ E(V−s)₊ ≤ sΞ(q)`) and a lower one `Θ` (`Θ = id` always valid); `ℓ₀ ≤ A`, `V ≤ V_max`.
   Conclusion (Theorem N1): Algorithm 2L⁺ with `Ξ(q)`, `Θ(p̲)` returns `L ≤ A ≤ U ≤ e^{x_out}L`,
   `x_out = ln[κ₀ + e^b(e^λ(1+η)/(1−η) + η′ + θ)]`, failure `δ`, cost `C_max` of Theorem 11.56 with
   `π_* = sup{π : Ξ(q) ≤ θ(1−η)ν₀q, Ξ(q) ≤ θ·max(c_ηq, Θ(c_ηq)) ∀q < π}`.  Replaced: Harper's `E_r` → `Ξ`; Harper term →
   `Θ`; `(2p_u)^n` → free `κ₀ ≤ 1`; `2un` → `ln(V_max/s₀)`; atoms → nothing (termination by the cap, or by the closing
   level: Theorem N1′, no cap); integrality → nothing.  The cube reproduces every constant of 11.56 exactly (10 sets).
   Variants: product blocks (N3), dependence with class-relative influence `ι` — slope `u → u + ι` (N4), base family
   (N2), exponent of a level and assembly (N5, N6).  2 624 simulated runs in valid settings, no violation.
2. **Exponent level (N3).**  A profile `w` with `w + id` strictly decreasing gives a `HintPair` (all Lean fields);
   convexity adds the game function `J = min_θ[θ + tw]`.  The shear identity is a hypothesis, not a tautology.
   Heterogeneous: recursion over arbitrary splits; no split undercuts `R̂`, proportional split is a fixed point
   (proved); best two-level outer block is not proportional (numerical).
3. **Instances.**  (a) cube: exact, identical constants.  (b), (c) biased cube, alphabets: sharp at the exponential
   scale via the report's Theorems 11.63/11.97(c); level theorem now a corollary; bounded accuracy open.  (d)
   site-dependent slopes: sharp via site types and a sandwich; explicit sorted-slope bound valid, not sharp.  (e)
   continuous sites: ball-volume and transport bounds valid, not sharp; transport useless for closing;
   discretisation gives upper bounds.  (e′) Gauss space with the sum metric: exact tail functions, extensivity,
   Gaussian pair exactly; lower bound open.  (f) chain: nesting valid with one-sided slack; no cost statement.
4. **Obstructions.**  Euclidean Gauss space: exact dimension-free tail functions; level operator `≥ max(T, Θ_na)`;
   every run draws `≥ (2K/(1+η))e^{(L−√(2x_out))²/2}` outer points at a linear instance (fixed split); hinted lower
   bound holds for `n ≥ L(L+1.29)²t` by ball dips; random blocks open.  Unbounded influence: (F2) fails by `e^{kc−u}`;
   80/80 invalid brackets on a 12+16-site instance; valid at enumeration cost with the true class.  Unbounded
   oscillation: exponential moment necessary and sufficient; closing level replaces the cap.
5. **Table (25 rows):** E 6, P 7, C 6, W 7, X 7, F 3; "not known" in 7 rows.  Most consequential: the sum metric
   (cost-only in the proof, the whole gain); (F2)/bounded influence (the only source of false certificates); the
   isoperimetric input (concentration is not enough; bounded accuracy needs a two-sided estimate, known only for
   the uniform cube and Gauss space).
6. **Weakest link:** Proposition N6 (assembly checked, not rewritten); N1′ tested only on small Gaussian instances.
7. **Errors:** five in the brief's sketch (lower tail function missing; role of oscillation and atoms; identity
   not by construction; Gaussian claim trivial as stated and no trivial bracket there; pointwise influence not
   sharp), two stale or too pessimistic remarks in the theory report (§11.18 remark (3)); none in the proofs of
   11.52/11.56.
8. **Files:** `docs/workstreams/N_REPORT.md`; `experiments/workstreams/N/{nlib,n1…n5}.py` with five outputs.
