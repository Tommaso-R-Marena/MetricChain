# Phase II — the adaptive hierarchy: how many rounds does the optimal exponent need?

*Division: Phase II, adaptive hierarchy (branch `research/phase2-adaptive-hierarchy`, based on the pinned
theory commit `b3c5d6115df06bb160d6490a95d9ec6e1a108d02`; consolidated archive read at
`fe9f58c1f0bfe5de8c6434c3490a33cd1d94023f`).  Written 2026-11-28 by one AI session.  Status labels as in
the theory division: **[V]** machine-checked, **[P]** paper proof in this file, **[N]** numerical evidence
(script named), **[K]** quoted from the archive (with its own status), **[C]** conjecture.  "Reviewed"
below always means reviewed by another AI session.  Nothing here has been read by a human expert.*

*Later additions (same day), each marked where it occurs: the independent replication by the engineering
division (`ENG-RES-0020` on `research/phase2-certified-inference`) and the corrections it led to (§3, §4);
the outcome of the reviews (§12); and `HIERARCHY_ADDENDUM.md`, which extends Theorem H1 from known blocks to
**hidden partitions** (Theorems P and H6 there) and settles open problems 1 and 2 of §8 for bounded
structure.  Read the addendum together with this report: §0, §8 and §10 are stated here as updated by it.*

*Resource note.  This session cannot see its own expenditure.  The work was therefore kept bounded:
one line of attack at a time, all computations on the local container (no external compute, no Modal
request), two reviewing subagents (one for this report, one for the addendum), each used once.  It stops at completion and does not resume when a message arrives.*

---

## 0. What was asked, and what is established

**The problem.**  `Q_n = {0,1}^n`, `L_u` the energies `ψ` with `|ψ(x) − ψ(x′)| ≤ u` for neighbours,
`A(ψ) = 2^{−n} Σ_x e^{−ψ(x)}`.  A randomised algorithm evaluates `ψ` at points of its choice, in at most
`k` batches (*rounds*; a batch may depend on the answers to the earlier ones), and returns a bracket of
ratio `e^ε` that contains `A(ψ)` with probability `1 − δ`.  `c_k(u)` is the exponent of the least number
of evaluations.  Known from the archive: `c_1 = a` [V lower bound, P upper], `c_∞ = h` [V lower, P upper],
`h < θ₂* ≤ c_2 ≤ T^{(2)}(0) < a` [P], and nothing above `h` for three rounds: the "three-block chain"
that continues the two-round family numerically hides nothing (workstream U §2.4, small-slope limit, one
family).  Is every fixed number of rounds suboptimal, or do finitely many rounds reach `h`?

**Answer obtained here (for the class on which every known lower bound lives).**  Let `BR_m` be the
*block-radial* energies on `m` known blocks with hidden centres (definition in §1; it contains the radial
functions, the cones and dips of the one-round and hinted lower bounds, the two-round twins of Theorem
11.86, and the three-block chain).

| | statement | status |
|---|---|---|
| **H1** | **Three rounds suffice on every block-radial class.**  For every `u`, `m`, every partition into `m` blocks of size at least a constant `N_u`, and every `η > 0` there is a three-round algorithm that, for all large `n` and every `ψ ∈ BR_m`, returns a valid bracket of any prescribed ratio with probability `1 − δ` from at most `e^{n(h+η)}` evaluations.  Hence `c_3(BR_m) = h = c_∞(BR_m)`.  (Blocks of any size, and unknown: Theorem H6 of the addendum.) | [P] §4, for `n ≥ n₀(u, m, η, ε, δ)`; lower bound [K: Theorem 11.25, V]; simulation and cube-level tests [N] |
| **Lemma B** | *The relaxation lemma* behind H1: if a block-radial energy shows, to a blind batch of `e^{nθ}` points, dependence on the blocks `P` only, and, to a batch that knows the centres of `P`, dependence on `P ∪ Q` only, then **every** type that is atypical in the remaining blocks `T` beyond the budget carries at most `e^{n(h−θ)+O(log n)}` times the largest mass a blind batch sees.  "What two rounds do not reveal carries no mass." | [P] §3, complete at finite `n` with explicit constants; exact check on extremal functions [N] |
| **H2** | **The two-round exponent of two blocks, exactly:** `c_2(BR_2(φ_1, φ_2)) = max{h, ϑ(φ_1), ϑ(φ_2)}`, with `ϑ(φ) = min{(1−φ)a, root of Ξ(·, φ)}` the threshold of Theorem 11.86.  The lower bound is the archive's; the matching upper bound — the step the archive left as "numerical" in its conjecture (U_REPORT §3.4, §8 item 2) — is proved here, for bounded accuracy. | [P] §5; lower bound [K: Theorem 11.86, P refereed; coupling V] |
| **Hierarchy** | On block-radial classes the round hierarchy has **at most three levels, and exactly three whenever some group of blocks is a fraction below `1 − h/a` of the cube**: `a` (one round), a value in `(h, a)` equal to `θ₂*(u)` at the best two-block split (two rounds), and `h` from three rounds on.  At `u = 1`: `0.1109`, `0.0399`, `0.0291`.  For a fixed class the middle level can coincide with `h` (two equal blocks when `u ≳ 6.1`), and `c_2(BR_m)` is not determined for `m ≥ 3`. | corollary |
| **Barrier** | Consequently **no application of the archive's hiding lemma (Lemma 11.85: twins that a batch cannot tell apart even when it is handed the centres of the earlier levels) to block-radial energies on a bounded number of blocks can show `c_3(u) > h`,** for any `u`, any split, any profile; more generally for `m` blocks of size at least `N_u` with `m·ln n = o(n)`.  The failure of the three-block chain is not a matter of parameters.  The bound on `m` is essential (with one-coordinate blocks `BR_n = L_u`), and Lemma 11.85 does not model hidden partitions; for those see the addendum (Corollary H8). | corollary of Lemma B |
| **Beyond blocks** | (i) In the small-slope limit the same obstruction holds for "flags" of hidden directions with *any* admissible Lipschitz body (centres that overlap instead of living in disjoint blocks), for every number of rounds `r ≥ 3`, with a margin `√θ(2√θ − 1)/4` in the exponent for `θ > ¼`.  (ii) Exponentially many indistinguishable copies of a hidden structure ("a code of cells") dilute the later rounds, but cost the adversary the same exponent in mass; the relaxation argument survives, with a positive margin for `θ > h`. | (i) [P] for the limit model, §7.1; (ii) [P] at the level of exponents, §7.2; both with [N].  The margins are the reviewer's (§12); as first written both proofs gave only "`≤`". |
| **Addendum: P, H6** | **Three rounds suffice for every energy with a bounded hidden symmetry type**: `c_3(HP_m) = h`, where `HP_m` are the energies in `L_u` that are functions of the numbers of ones in the classes of an *unknown* partition of the coordinates into at most `m` classes (hidden blocks and centres; any bounded number of hidden centres with arbitrary overlaps; merged and nested blocks).  Behind it: the relaxation principle for arbitrary nested hidden partitions (Theorem P), with a short, dimension-free proof. | [P] `HIERARCHY_ADDENDUM.md` §A2–A5, finite `n`; brute-force and cube-level checks [N]; arithmetic [V] |
| **Verification** | The two-round separation (priority 1) was re-derived and recomputed with own code: the thresholds `θ₂*(u)` at eight slopes and the exact finite-`n` twins reproduce the archive's tables digit for digit; the two Lean files of the coupling lemma build with the pinned toolchain. | §2 [N], [V] |

**What is not established.**  Whether `c_3(u) = h` on all of `L_u`.  H1 and H6 are *upper bounds on
subclasses*, and the barrier is a statement about families of bounded structure; neither decides the
general question.  We state the conjecture `c_3(u) = h(u)` (§8) and what a proof or a refutation would
have to look like.  The honest summary is: **the question "is every fixed number of rounds suboptimal" is
answered negatively on every class of energies with a bounded hidden symmetry type — three rounds are
optimal there, and the algorithm is not told the structure — and remains open on `L_u`, where a
separation would need hidden information spread over a number of classes that grows with `n`, and a
collapse would need an algorithm for energies with no symmetry at all.**

---

## 1. Setting and notation

`u > 0` is fixed.  `f(ρ) = KL(ρ‖½)`, `p_u = 1/(1+e^u)`, `Λ₁ = ln(2/(1+e^{−u}))`, `k(ρ) = KL(ρ‖p_u) =
f(ρ) + uρ − Λ₁`, `a = f(p_u)`, `κ = Λ₁/u`, `h = f(κ)` (so `k(κ) = h`), `D(θ) = u f^{−1}(θ) − Λ₁`
(`D(h) = 0`, `D` decreasing and convex, `D′ ≤ −1` on `[h, a]` because `|f′| ≤ u` on `[p_u, ½]`).

**Blocks and types.**  `[n] = B_1 ⊔ … ⊔ B_m`, `n_j = |B_j|`, `φ_j = n_j/n`.  A *centre* is
`s = (s¹, …, s^m)`, `s^j ∈ {0,1}^{B_j}`; the *type* of `x` is `d = (d(x¹, s¹), …, d(x^m, s^m)) ∈ 𝒟 = Π_j {0..n_j}`.
A *profile* `F : 𝒟 → ℝ` is *admissible* if `|F(d) − F(d′)| ≤ u` whenever `d, d′` differ by one in one
coordinate; then `|F(d) − F(d′)| ≤ u‖d − d′‖₁` and `ψ_{F,s}(x) = F(type of x) ∈ L_u`.

    BR_m(B_1..B_m) = { ψ_{F,s} : F admissible, s a centre }          (blocks known, centres and profile hidden).

`P_j(d) = C(n_j, d) 2^{−n_j}`, `P(d) = Π_j P_j(d_j)`, and `A(ψ_{F,s}) = Σ_d P(d) e^{−F(d)}` does not depend on
`s`.  `d_j* = ⌊n_j/2⌋`.  We measure the cost of a type *relative to the typical type*:

    t_j(d) = ln P_j(d_j*) − ln P_j(d) ≥ 0,     t_S(d) = Σ_{j∈S} t_j(d_j),     t = t_{[m]},
    ν(d)  = −F(d) − t(d)                    (so that P(d) e^{−F(d)} = P(d*) e^{ν(d)}),
    V_S(Θ) = { d ∈ 𝒟 : t_{S^c}(d) ≤ Θ }      (S ⊂ [m]; the types a batch sees that knows the centres of S).

`L = ln(n+1)`.  Elementary facts used throughout (`γ_j(d) := t_j(d) + u·d`):

* (F1) `|t_j(d) − n_j f(d/n_j)| ≤ L`; `t_j` is symmetric about `n_j/2`, nonincreasing on `[0, d_j*]`.
* (F2) `γ_j(d) ≥ n_jΛ₁ − L` for every `d` (from `Σ_d P_j(d) e^{−ud} = e^{−n_jΛ₁}`).
* (F3) `γ_j(y) ≥ γ_j(e)` for integers `y ≤ e ≤ (n_j+1)p_u` (because `γ_j(d) − γ_j(d+1) = ln((n_j−d)/(d+1)) − u`).
* (F4) Let `k_j = ⌈κ n_j⌉` and assume `n_j ≥ N_u := ⌈5/(1−2κ)⌉`, so that `k_j ≤ d_j* − 1`.  For integers
  `(n_j+1)p_u < e ≤ k_j`: `γ_j(e) ≤ n_j(Λ₁ + k(e/n_j)) + L ≤ n_jΛ₁ + n_j h + u + L` (`k` is nondecreasing on
  `[p_u, ½]`, `k(κ) = h`, `k′ ≤ u` there).
* **(R)** Hence for integers `0 ≤ y ≤ e ≤ k_j`: `γ_j(e) ≤ γ_j(y) + n_j h + u + 2L`.
  (If `e ≤ (n_j+1)p_u` by (F3); otherwise by (F4) and (F2).)

**Rounds.**  An `r`-round algorithm asks `r` batches; `c_r(𝒞)` denotes the exponent of the least number of
evaluations with which a bounded accuracy is reached on the class `𝒞` (`limsup` for upper, `liminf` for lower
bounds, as in the archive).  All algorithms below are valid for every `ψ` of the class, in every run up to
the stated failure probability, and their cost is bounded by a deterministic number.

---

## 2. Priority 1 — the two-round separation, verified independently

Theorem 11.86 (= U3) of the archive: for `φ₁, θ` with `Ξ(θ, φ₁) > 0` and `θ < φ₂a`, two batches need
`max(M₁, M₂) ≥ (1−2δ) e^{nθ}/(2(n+1)²)`; `θ₂*(u) = max_{φ₁} ϑ(φ₁) > h`.

* **Re-derivation.**  The mechanism was re-derived independently in the small-slope coordinates of §7.1
  (there: on the blind disc the deepest admissible function is the flat histogram of the first block; the
  hidden cone at the vertex `(σ₁, σ₂)` casts the shadow `2⟨X, e⟩ − 1` on the anchors `e`; the gain is
  `1 + min_c [c − 2√(φ₁c) − 2√(φ₂(θ−c))]`).  The archive's finite-slope proof (U_REPORT §2.2, steps (1)–(4))
  was read step by step; no error found.  Its estimate of the gap is moreover confirmed *from the other
  side*: §5 proves that `min{Ξ(θ, φ₁), φ₂k(y¹)}` — the archive's lower bound for the gap of its twins — is an
  upper bound for the hidden gain of **every** two-block function whose first block alone is revealed in
  round one (Lemma A2).  The twins are extremal.
* **Thresholds recomputed** [N] (`experiments/phase2_hierarchy/h2_two_round_verify.py`, part A; own
  minimisation and bisection, nothing imported): `θ₂*/a = 0.3460, 0.3469, 0.3495, 0.3594, 0.3940, 0.4396,
  0.4878, 0.5749` and best `φ₁ = 0.654, 0.653, 0.651, 0.641, 0.606, 0.560, 0.512, 0.425` at
  `u = 0.05, 0.25, 0.5, 1, 2, 3, 4, 6` — the archive's table (U_REPORT §2.2) in every printed digit.  (The
  reviewer's own computation to six digits gives `0.3461` at `u = 0.05` and `0.39408` at `u = 2`: the fourth
  digit of the archive's table and of ours is one unit low at these two slopes.  The agreement is real, the
  last digit is not.)
* **Exact finite-`n` twins rebuilt from scratch** [N] (same script, part B): the twins are constructed here
  as *the deepest admissible functions under the visibility constraints* (a different description from the
  archive's formulas), exact binomial arithmetic, all structural checks on (admissibility, equality on `V₂`,
  dependence on `d₁` only on `W₁ ∩ V₂`).  With the archive's choice of the shallow twin the table of
  U_REPORT §2.2 is reproduced exactly: `u = 1`: `(n, n₁, gap, E, E/h) = (400, 200, 1.05, 0.03190, 1.095),
  (800, 400, 1.07, 0.03387, 1.162), (1600, 880, 1.04, 0.03598, 1.235), (3200, 1760, 1.01, 0.03661, 1.256)`;
  `u = 2`: `(200, 90, 1.05, 0.11165, 1.148), (400, 200, 1.16, 0.11570, 1.189), (1600, 880, 1.05, 0.12244, 1.259)`.
  (With the shallow twin capped by the flat histogram instead — also a valid pair — `E` is lower by
  `0.0002`–`0.0015`.)  Output: `out/h2_two_round_verify.txt`.
* **Machine-checked part.**  `proofs/Frontiers/TwoRounds.lean` and `TwoRoundsExpected.lean` (the coupling
  lemma for two rounds, deterministic and expected batch sizes) were built here with the pinned toolchain
  (Lean 4.31.0, Mathlib v4.31.0 from the cache): `Build completed successfully (8559 jobs)`.  [V]  The
  application to the cube (the twins and their gap) is a paper proof with exact computations, as the
  archive says.
* **Simulation.**  In the type-level simulation of §6 a two-round algorithm with `M` points per shell misses
  `0.45`–`0.51` nats of `ln A` on the deep twin (`n = 1200`, `u = 2`, blocks `(720, 480)`, designed against
  `Θ_c = 1.15nh`) for `ln M` up to `Θ_c − 8`, and the three-round algorithm does not.

**Verdict.**  The two-round separation stands; `c_2(u) ≥ θ₂*(u) > h` for every `u`.

---

## 3. The relaxation lemma

Throughout this section `F` is admissible, `P ⊔ Q ⊔ T = [m]` (any of the three may be empty), all blocks
have `n_j ≥ N_u`, and `Θ ≥ nh + 2mL`.

*Hypotheses.*  For `S ⊂ [m]` and a set `V` of types say that **`F` sees only `S` on `V`** if `F(d) = F(d′)`
for all `d, d′ ∈ V` with `d_S = d′_S` and `d_j ≡ d′_j (mod 2)` for every `j ∉ S`.  (The parities cannot be
dispensed with: a profile that is 2-periodic in `d_j` shows the same value at all neighbours of a point in
block `j`, so its centre is not revealed, yet it depends on `d_j`.)

 (H1) `F` sees only `P` on `V_∅(Θ)`.          (H2) `F` sees only `P ∪ Q` on `V_P(Θ)`.

`ν₀ := max{ν(d) : d ∈ V_∅(Θ)}` — the largest mass a blind batch of budget `Θ` sees, in units of `P(d*)`.

> **Lemma B (relaxation).**  Under (H1), (H2), for every type `y ∈ 𝒟`:
>
>     ν(y) ≤ ν₀ + n φ_P h − min{ t_T(y), Θ − n(1 − φ_P) h } + m(u + 5L).
>
> In particular every `y` with `t_T(y) > Θ − n(1−φ_P)h` — a fortiori every `y ∉ V_{P∪Q}(Θ)` — satisfies
> `ν(y) ≤ ν₀ − (Θ − nh) + m(u + 5L)`.

In exponents (`Θ = nθ`, `ν = n·`mass exponent): *types that a third batch, which knows `P ∪ Q`, cannot
reach have mass at most `e^{n(h − θ)}` times the blind-visible maximum.*  Note what is **not** assumed:
nothing about `F` outside the two regions, nothing about how `F` depends on `P`, on `Q`, or — beyond
`V_P(Θ)` — on `T`.

**Proof.**  *Reduction.*  Reflecting a block, `d_j ↦ n_j − d_j`, preserves `t_j`, admissibility, the regions
and both hypotheses (parity classes go to parity classes).  So assume `y_j ≤ d_j*` for all `j`.

*The anchor.*  Put `e_j = max(y_j, k_j)` for `j ∈ P ∪ Q`, and `e_j = max(y_j, ⌈τ n_j⌉)` for `j ∈ T`, with
`τ ∈ [0, κ]` chosen as follows.  By (F1), `t_j(e_j) ≤ t_j(k_j) ≤ n_j h + L` for `j ∈ P ∪ Q`; let
`Θ₂ = Θ − nφ_Q h − mL`.  The function `τ ↦ T(τ) = Σ_{j∈T} t_j(max(y_j, ⌈τn_j⌉))` is nonincreasing on `[0, κ]`,
a left-continuous step function whose jumps are at most `|T|·L`, with `T(0) = t_T(y)` and
`T(κ) ≤ nφ_T h + mL ≤ Θ₂`.
 (i) If `t_T(y) ≤ Θ₂` take `τ = 0` (`e_T = y_T`).
 (ii) Otherwise take `τ` just to the right of `inf{τ : T(τ) ≤ Θ₂}`; then `Θ₂ − mL < t_T(e) ≤ Θ₂`.
In both cases `t_Q(e) + t_T(e) ≤ Θ`, i.e. `e ∈ V_P(Θ)`.

*The value at the anchor is a blind-visible value.*  Let `w_j ∈ {d_j*, d_j* − 1}` have the parity of `e_j`
(`t_j(w_j) ≤ ln 3 ≤ L`).  `e′ := (e_P, e_Q, w_T) ∈ V_P(Θ)`, so `F(e) = F(e′)` by (H2).  `e′` and
`e″ := (e_P, w_Q, w_T)` lie in `V_∅(Θ)` (`t(e′) ≤ n(φ_P+φ_Q)h + 2mL ≤ Θ`), so `F(e′) = F(e″)` by (H1).  And
`ν(e″) ≤ ν₀` gives `−F(e″) ≤ ν₀ + t(e″) ≤ ν₀ + t_P(e) + mL`.

*Lipschitz.*  `−F(y) ≤ −F(e) + u Σ_j (e_j − y_j)`.  Therefore

    ν(y) ≤ ν₀ + mL + Σ_{j∈P} [γ_j(e_j) − γ_j(y_j)] + Σ_{j∈Q∪T} [u(e_j − y_j) − t_j(y_j)].

*The three kinds of terms.*
 `j ∈ P`: zero if `e_j = y_j`; if `e_j = k_j > y_j`, at most `n_j h + u + 2L` by (R).
 `j ∈ Q`: `−t_j(y_j) ≤ 0` if `e_j = y_j`; if `e_j = k_j > y_j`: `u k_j − γ_j(y_j) ≤ u(κn_j + 1) − n_jΛ₁ + L = u + L`
 by (F2) — *relaxing a block to the hinted radius `κ` is free*, because `uκ = Λ₁`.
 `j ∈ T`: `−t_j(e_j)` if `e_j = y_j`; if `e_j = ⌈τn_j⌉ > y_j` (so `e_j ≤ k_j`):
 `u(e_j − y_j) − t_j(y_j) = γ_j(e_j) − γ_j(y_j) − t_j(e_j) ≤ n_j h + u + 2L − t_j(e_j)` by (R) — *relaxing a block
 to a radius deeper than `κ` earns the excess of its cost over `h`.*
Summing, with `T_rel` the relaxed blocks of `T`:

    ν(y) ≤ ν₀ + n h (φ_P + φ_{T_rel}) − t_T(e) + m(u + 3L).

In case (i), `T_rel = ∅` and `t_T(e) = t_T(y)`: `ν(y) ≤ ν₀ + nφ_P h − t_T(y) + m(u + 3L)`.  In case (ii),
`t_T(e) > Θ − nφ_Q h − 2mL` and `φ_Q + φ_{T_rel} ≤ 1 − φ_P`: `ν(y) ≤ ν₀ + nφ_P h − (Θ − n(1−φ_P)h) + m(u + 5L)`.  ∎

**Why the three-block chain had to fail.**  In the chain, block 1 is `P`, block 2 is `Q`, block 3 is `T`, and
the hidden dip is a type outside `V_{P∪Q}(Θ)`; the lemma bounds its mass by `e^{n(h−θ)}` times a visible
mass, for every slope, every split and every profile.  The archive's diagnosis ("round 2 has its full
budget on a smaller cube") is the special case of the anchor in which `e_P = y_P`: the general anchor
*also relaxes the revealed blocks to the hinted radius*, at the price `nφ_P h`, which is exactly what the
`T`-blocks earn back by using the budget `Θ − nφ_Q h` instead of `nφ_T h`.

**Machine-checked bookkeeping** [V].  `proofs/Frontiers/RelaxationCore.lean` (namespace
`MetricChain.RelaxationCore`; built with the pinned toolchain; standard axioms only): `relaxation_core`
derives the displayed bound from the four per-block inequalities, the cap and the Lipschitz step —
exactly the inputs listed above, as hypotheses — and `relaxation_exhausted`, `relaxation_unmoved` are the
cases (ii) and (i); `relax_step` is (R) from (F2) and (F4); `choose_mul_pow_le` and `choose_step` are the
binomial facts (F2) and (F3) in exact form.  What is checked is the arithmetic of the proof (signs, which
sums cancel, the constants) and those two facts.  The entropy bounds (F1), (F4), the existence of the
anchor and the use of (H1), (H2) are **not** formalised.

**Exact check** [N] (`experiments/phase2_hierarchy/h1_relaxation_lemma_check.py`, output
`out/h1_relaxation_lemma_check.txt`).  For given blocks, roles and `Θ` the script builds the *pointwise
deepest* admissible function satisfying (H1), (H2) and `ν ≤ 0` on `V_∅(Θ)` — a bound that holds for it holds
for every function with these properties — and evaluates the left side of the lemma for all types with
exact binomial costs.  124 cases (`n = 200` to `360`; three and four blocks; role patterns `PQT, PTT, PPT,
QQT, QTT, PPQT, PQTT, PQQT, PTQT`; `u = 0.5, 1, 2, 4`; `θ/h ∈ {1, 1.1, 1.3}` for three blocks and `{1, 1.2}` for
four): the hypotheses and admissibility hold for every constructed function; the largest value of
`ν(y) − ν₀ − nφ_P h + min{t_T(y), Θ − n(1−φ_P)h}` is `+4.95` nats (at `u = 4`, `θ = h` exactly, a plain dip at
the critical budget), against the lemma's allowance `m(u + 5L) ≈ 100`.

*Corrections after an independent replication* (engineering division, `ENG-RES-0020`: own code written
from this report, cross-checked by Dijkstra and by linear programmes; 220 cases, these 124 and 96 others).
(1) The lemma's criterion holds in all 220 cases; largest value `+4.969` nats.  (2) The script imposes
plain independence of the other coordinates, which is a *stronger* hypothesis than (H1), (H2) as stated
above (independence up to parities); under the stated hypotheses the values are higher by up to `0.164`
nats.  (3) An earlier version of this paragraph said that at `θ ≥ 1.1h` the hidden types stay below
`ν₀ − n(θ − h) + 0.002` "without any logarithmic loss".  **That is withdrawn as a general statement**: it
holds on the 124 cases without parities only; with parities two of them give `+0.019`, and other splits
give up to `+0.617` nats (blocks `(30, 30, 50, 70)`, roles `QQTT`, `u = 1`).  An excess of the order of one
lattice step `u` is what Theorem P of the addendum predicts (there: at most `0.95·u` in entropy form).
(4) Every one of these cases lies *outside* the lemma's hypothesis `Θ ≥ nh + 2mL` (at these sizes that would
need `Θ` between two and four times `nh`), and some have a block below `N_u`: the computations test a
statement somewhat stronger than the lemma, at small sizes, and at `n ≤ 400` the allowance `m(u + 5L)` does
not separate valid from invalid profiles (the replication's negative controls reach it only near
`n = 1000`).  They show that the lemma is not false there and say little about its constants.  (5) The
script builds the extremal function by a fixed sequence of passes; the replication found it equal to the
exact fixed point on all 124 cases to print rounding.

---

## 4. Theorem H1 — three rounds suffice on block-radial classes

**Algorithm R3(M)** (blocks `B_1..B_m` known; `ψ = ψ_{F,s}` unknown).  A point `x` *reveals* block `j` if the
values `ψ(x^{(i)})`, `i ∈ B_j`, at its neighbours in that block are not all equal.  In that case they take
exactly two values (`F(d + e_j)` at the coordinates where `x` agrees with `s^j`, `F(d − e_j)` where it does
not); let `I ⊂ B_j` be the set of coordinates with the value attained at the least index of `B_j`, and
`c^j := x^{B_j} ⊕ 1_I`.  Then `c^j ∈ {s^j, s̄^j}` (`s̄` the antipode): a *centre candidate*.

* **Round 1.**  `M` independent uniform points; evaluate each with its `n` neighbours.  `S₁` := the blocks
  revealed by some point; fix a candidate `c^j` for each `j ∈ S₁`.
* **Round 2.**  For every *shell* `a ∈ Π_{j∈S₁}{0..n_j}`: `M` independent points `x` with `x^{B_j}` uniform
  on the sphere of radius `a_j` around `c^j` for `j ∈ S₁` and uniform on `{0,1}^{B_j}` for `j ∉ S₁`; evaluate
  each with its neighbours in the blocks outside `S₁`.  `S₂` := `S₁` together with the blocks revealed by
  some point of this round; candidates as before.
* **Round 3.**  For every shell `a ∈ Π_{j∈S₂}{0..n_j}`: `M` independent points as in round 2 with `S₂` in
  place of `S₁` (the set `X₃(a)`); evaluate them.
* **Output.**  `Â = Σ_a [Π_{j∈S₂} P_j(a_j)] · (1/M) Σ_{x∈X₃(a)} e^{−ψ(x)}` and the bracket `[Â e^{−ε/2}, Â e^{ε/2}]`.

Three rounds; at most `3(n+1)^{m+1} M` evaluations.  *Remark (unbiasedness).*  `Σ_a Π P_j(a_j) ·`(uniform on
the product of spheres) is the uniform distribution on the cube for **any** candidates, so `E Â = A(ψ)`
whatever rounds 1 and 2 did.  The reveal logic is needed for the variance only — i.e. for nothing but
Lemma B.

> **Theorem H1.**  Let `u > 0`, `m ≥ 1`, `η, ε, δ ∈ (0, 1)`, `Θ = n(h + η/2)` and `M = ⌈(n+1)^m e^{Θ + ηn/4}⌉`.
> There is `n₀(u, m, η, ε, δ)` such that for all `n ≥ n₀`, every partition of `[n]` into `m` blocks of sizes
> at least `N_u`, and every `ψ ∈ BR_m(B_1..B_m)`: Algorithm R3(M) makes at most `e^{n(h+η)}` evaluations in
> three rounds and `P( Â e^{−ε/2} ≤ A(ψ) ≤ Â e^{ε/2} ) ≥ 1 − δ`.
> Consequently `c_3(BR_m) = h`: the lower bound `c_r ≥ h` for every `r` is Theorem 11.25 [K, V], whose
> alternatives (the flat energy against dips on balls around a hidden point) are radial, hence in `BR_m`.

**Proof.**  For a revealed block replace `s^j` by `c^j` and reflect `F` in that coordinate if `c^j = s̄^j`;
nothing below changes.  A uniform point has type `d` with probability `P(d*) e^{−t(d)} ≥ (n+1)^{−m} e^{−t(d)}`;
a point of shell `a` in round 2 (round 3) has type `(a, D)` with `D` distributed by the product of the
`P_j`, `j ∉ S₁` (`j ∉ S₂`).

*Events.*  `E₁`: every `d ∈ V_∅(Θ)` is the type of a point of round 1.  `E₂`: for every shell `a` of round 2,
every `d ∈ V_{S₁}(Θ)` with `d_{S₁} = a` is the type of a point of that shell.  Each fails with probability at
most `(n+1)^m exp(−e^{ηn/4})`.  For round 3 let `N_d` be the number of points of `X₃(d_{S₂})` of type `d` and
`p_d = Π_{j∉S₂} P_j(d_j)`; `E₃`: `|N_d − Mp_d| ≤ (ε/8)Mp_d` for every `d ∈ V_{S₂}(Θ)` — by Chernoff's bound it
fails with probability at most `2(n+1)^m exp(−ε² e^{ηn/4}/192)`.  Finally let

    X_bad = Σ_{d ∉ V_{S₂}(Θ)} P_{S₂}(d_{S₂}) (N_d/M) e^{−F(d)},      A_bad = Σ_{d ∉ V_{S₂}(Θ)} P(d) e^{−F(d)} = E[X_bad | rounds 1, 2],

and `E₄`: `X_bad ≤ (4/δ)A_bad` (Markov: fails with probability at most `δ/4`).

*From the answers to the hypotheses of Lemma B.*  Let `j ∉ S₁` and `d ∈ V_∅(Θ)` with `1 ≤ d_j ≤ n_j − 1`.  On
`E₁` some point of round 1 has type `d`; it has neighbours of both types `d ± e_j` in block `j`, and it does
not reveal `j`: `F(d + e_j) = F(d − e_j)`.  **Claim: `F` sees only `S₁` on `V_∅(Θ)`.**  Let `d, d′ ∈ V_∅(Θ)` agree
on `S₁` and in the parities elsewhere.  Go from `d` to `d′` one block at a time in steps of `±2`, first
through the blocks with `t_j(d′_j) ≤ t_j(d_j)`, then through the others.  By the unimodality of every `t_j`,
each type on the way and each midpoint of a step has cost at most `max(t(d), t(d′)) ≤ Θ`, and a midpoint
has its moving coordinate in `[1, n_j − 1]`; so no step changes `F`.  In the same way, on `E₁ ∩ E₂`, `F` sees
only `S₂` on `V_{S₁}(Θ)`.  So (H1), (H2) hold with `P = S₁`, `Q = S₂ ∖ S₁`, `T = [m] ∖ S₂`.

*The unseen types are negligible.*  For `d ∉ V_{S₂}(Θ)`, i.e. `t_T(d) > Θ`, Lemma B gives
`ν(d) ≤ ν₀ − (Θ − nh) + m(u + 5L) = ν₀ − ηn/2 + m(u+5L)`.  As `A ≥ P(d*) e^{ν₀}`,

    A_bad ≤ (n+1)^m e^{m(u+5L)} e^{−ηn/2} · A =: β_n A,        β_n → 0.

*The estimate.*  `Â = Σ_d P_{S₂}(d_{S₂})(N_d/M)e^{−F(d)}`, and `P_{S₂}(d_{S₂}) p_d = P(d)`.  On `E₃` the part of
the sum over `V_{S₂}(Θ)` lies in `(1 ± ε/8)(A − A_bad)`; on `E₄` the rest is at most `(4/δ)A_bad`.  Hence on
`E₁ ∩ … ∩ E₄`

    (1 − ε/8)(1 − β_n) A ≤ Â ≤ (1 + ε/8 + 4β_n/δ) A,

which is inside `[e^{−ε/2}A, e^{ε/2}A]` as soon as `β_n(1 + 4/δ) ≤ ε/8`.  The four events fail with total
probability at most `δ/4 + 4(n+1)^m exp(−ε² e^{ηn/4}/192) ≤ δ` for large `n`, and
`3(n+1)^{m+1}M ≤ e^{n(h+η)}` for large `n`.  ∎

*Remarks.*  (1) The accuracy is in fact `1 + o(1)`: any fixed `ε` works from some `n` on.  (2) Blocks smaller
than `N_u` (a constant) are excluded only to keep (F4) clean.  (3) The number of blocks may grow with `n` as
long as `m ln n = o(n)`; the proof is unchanged.  (4) The block partition is *known* to the algorithm.
For a hidden partition the reveal step identifies the coordinates of a block together with its centre
only when the profile separates the blocks; when it does not (a profile that depends on `d_1 + d_2` on
what is seen) the algorithm controls only a sum of block distances, and the relaxation lemma has to be
proved for that information structure.  §7.1 does this in the small-slope limit; at finite slope it is
open (§8).

*On real cubes* [N] (`experiments/phase2_hierarchy/h7_r3_on_cubes.py`, output `out/h7_r3_on_cubes.txt`).
Algorithm R3 run literally (points, neighbours, candidates, shells) on energies given as tables on
`Q_12`–`Q_14`, three kinds of profiles (minima of cones; a profile 2-periodic in one block; a profile that
depends on a block only next to its centre), `M ∈ {3, 30}`, 60 runs each: every candidate is the centre or
its antipode; the estimate is exact whenever all blocks on which the profile depends are revealed; it is
unbiased otherwise (`|z| ≤ 2.4` in the six cases with a 2-periodic block, which is never revealed); the
mutation "uniform shell weights" is caught in all 18 cases; the mutation "reveal nothing" stays unbiased,
as the remark above says it must.  These sizes test the logic of the algorithm, not its exponent.
*Independent replication* (`ENG-RES-0020`, own code): 32 instances with `n = 12…16`, `M` up to `10⁵`, 39 056
runs — the candidate of a revealed block is the centre or its antipode without exception, the estimate
is exact whenever all blocks are revealed, the conditional mean of the estimate over all `2ⁿ` points equals
`A(ψ)` to `10⁻¹⁴` in every run, and the mutation is caught in 99 of 100 tests.

---

## 5. Theorem H2 — the two-round exponent of two blocks, exactly

`m = 2`.  `Ξ(θ, φ₁) = min{ φ₁k(z) + φ₂(uρ − Λ₁) : z ∈ [p_u, ½], φ₁f(z) + φ₂f(ρ) ≤ θ }` (the function of
Theorem 11.86; decreasing in `θ`, positive at `θ = h`), `ϑ(φ₁) = min{φ₂a, root of Ξ(·, φ₁)}`.

> **Lemma A2 (two-round anchors).**  Let `F` be admissible on two blocks, `Θ > 0`, and suppose `F` sees only
> block 1 on `V_∅(Θ)`.  Let `ν₁ = max{ν(d) : d ∈ V_{1}(Θ)}` (the largest mass seen by a batch that knows
> `s¹`).  Then for every type `y` with `t₂(y₂) > Θ`:
>
>  (A1) `ν(y) ≤ ν₁ + n·Ξ(θ⁻, φ₁) + 2u + 4L`, where `θ⁻ = (Θ − 2L)/n`;
>  (A2) if `(Θ − L)/n₂ ≥ a`:  `ν(y) ≤ ν₁ − n₂·k(y¹) + u + 2L`, where `y¹ = f^{−1}((Θ − L)/n₂) ≤ p_u`.

**Proof.**  Reflect so that `y_j ≤ d_j*`.  (A1) Let `z ∈ [p_u, ½]`, `ρ` with `n[φ₁f(z) + φ₂f(ρ)] ≤ Θ − 2L` and put
`e = (max(y₁, ⌈zn₁⌉), ⌈ρn₂⌉)`.  By (F1) `t(e) ≤ Θ`, so `e ∈ V_∅(Θ)` and `e₂ > y₂`.  With `w₂ ∈ {d₂*, d₂* − 1}` of
the parity of `e₂`: `F(e) = F(e₁, w₂)`, and `(e₁, w₂) ∈ V_{1}(Θ)` gives `−F(e) ≤ ν₁ + t₁(e₁) + L`.  So

    ν(y) ≤ ν₁ + L + [γ₁(e₁) − γ₁(y₁)] + [u e₂ − γ₂(y₂)] ≤ ν₁ + L + [n₁k(z) + u + 2L] + [n₂(uρ − Λ₁) + u + L]

(the first bracket is `0` if `e₁ = y₁`, and otherwise bounded by (F1), (F2); the second by (F2)).  Minimise
over `(z, ρ)`.  (A2) The anchor `e = (y₁, ⌈p_un₂⌉)` lies in `V_{1}(Θ)`, so `−F(e) ≤ ν₁ + t(e)` and
`ν(y) ≤ ν₁ + γ₂(e₂) − γ₂(y₂)`, with `γ₂(e₂) ≤ n₂Λ₁ + u + L` and, because `t₂(y₂) > Θ` forces `y₂/n₂ < y¹ ≤ p_u`
and `k` decreases on `[0, p_u]`, `γ₂(y₂) ≥ n₂Λ₁ + n₂k(y¹) − L`.  ∎

The archive proves that its twins have a gap of at least `n·min{Ξ(θ, φ₁), φ₂k(y¹)} − o(n)` when `θ < φ₂a`
(there `y¹ > p_u`).  Lemma A2 and its mirror image say that **no** two-block function whose first block
alone is revealed in round one hides more than `n·min{Ξ, φ₂k(y¹)}₊ + O(log n)` — (A2′): for `θ < φ₂a` the
anchor `(y₁, ⌈y¹n₂⌉)` gives `ν(y) ≤ ν₁ + n₂[k(y¹) − k(y₂/n₂)] + O(L) ≤ ν₁ + n₂k(y¹) + O(L)`.  So the twins are
extremal, and the step that the archive recorded as numerical ("the supremum over `x` … attained at
`x = p_u`") is this lemma.  Exact gaps of the twins at `n = 3200, 6400` stay below the formula, as they
must (`out/h2_two_round_verify.txt`, part C).

**Algorithm R2(M)**: rounds 1 and 2 of R3, round 2 without neighbours, and
`Â₂ = Σ_{a ∈ Π_{j∈S₁}{0..n_j}} [Π_{j∈S₁} P_j(a_j)] (1/M) Σ_{x∈X₂(a)} e^{−ψ(x)}`.

> **Theorem H2.**  Let `0 < φ₁ < 1`, `φ₂ = 1 − φ₁`, `θ* = max{h, ϑ(φ₁), ϑ(φ₂)}`, and let the two blocks have
> `n_j/n → φ_j`.  (a) For every `η > 0`, `ε, δ ∈ (0,1)` and all large `n`, Algorithm R2 with
> `M = ⌈(n+1)² e^{n(θ* + η)}⌉` returns, for every `ψ ∈ BR_2`, a bracket of ratio `e^ε` that contains `A(ψ)` with
> probability `1 − δ`, from at most `e^{n(θ* + 2η)}` evaluations in two rounds.  (b) [K: Theorems 11.25 and
> 11.86] no two-round algorithm does it with `e^{n(θ* − η)}`.  Hence
>
>     c_2(BR_2(φ₁, φ₂)) = max{ h, ϑ(φ₁), ϑ(φ₂) },          sup_{φ₁} c_2(BR_2(φ₁, 1−φ₁)) = θ₂*(u).

**Proof of (a).**  Put `Θ = n(θ* + 3η/4)`; events `E₁`, `E₃`, `E₄` as in the proof of Theorem H1 with `S₁` in
place of `S₂` and "bad" meaning `t_{S₁^c}(d) > Θ`.  On `E₁`, `F` sees only `S₁` on `V_∅(Θ)`.
`S₁ = {1, 2}`: there is no bad type and `Â₂ = A` exactly.
`S₁ = ∅`: Lemma B with `P = Q = ∅`, `T = {1,2}` (its hypotheses coincide): every bad type has
`ν ≤ ν₀ − (Θ − nh) + 2(u + 5L)`.
`S₁ = {1}`: `Θ/n ≥ ϑ(φ₁) + 3η/4`, so either `Θ/n ≥ φ₂a + 3η/4` and (A2) gives `ν ≤ ν₁ − n₂k(y¹) + O(L)` with
`k(y¹)` bounded below by a positive constant, or `Θ/n ≥ root + 3η/4` and (A1) gives
`ν ≤ ν₁ + nΞ(θ⁻, φ₁) + O(L)` with `Ξ(θ⁻, φ₁)` bounded above by a negative constant (monotonicity of `Ξ` in `θ`).
`S₁ = {2}`: the same with the blocks exchanged.
In every case `A_bad ≤ e^{−cn}A` for a constant `c = c(u, φ₁, η) > 0` and large `n`, and the estimate is
analysed as before.  ∎

*For more than two blocks* Theorem 11.86, applied to two disjoint groups of blocks, gives `c_2(BR_m) ≥` the
best of the two-block thresholds over all such pairs (rescaled to the sub-cube they span) — a lower bound
from the archive, not from the proof above — and we expect equality and
`c_2(BR_m) ≤ θ₂*(u)`; the anchor argument for a hidden group in which only some blocks are deep needs one
more case distinction, which we did not complete.  **[C]**

---

*Remark.*  The lower-bound half of Theorem H2 is Theorem 11.86 and inherits its conditions (`δ < ½`,
`n₁ = ⌊φ₁n⌋`); for block sizes with `n_j/n → φ_j` one needs its threshold `n₀` locally uniform in `φ₁`, which
is plausible and not stated in the archive.

## 6. The hierarchy on block-radial classes, and a simulation

**Corollary H3.**  For every `u > 0` and every two-block class with `φ₁ < 1 − h/a`:
`c_1 = a > c_2 = max{h, ϑ(φ₁), ϑ(φ₂)} > h = c_3 = c_4 = …`; the supremum of `c_2` over splits is `θ₂*(u)`.
For every `m`: `c_1(BR_m) = a` (cones against truncated cones are radial; Theorems 11.44/11.45 [K]),
`c_r(BR_m) = h` for all `r ≥ 3`, and `h < c_2(BR_m) < a` whenever some group of blocks has a fraction
`φ < 1 − h/a` (a function that is radial in a group of blocks is block-radial, so `BR_m` contains the two-block
classes of all groupings and `c_2(BR_m) ≥ ϑ(φ) > h`; `c_2 ≤ T^{(2)}(0) < a` is Corollary 11.87 [K], valid on
all of `L_u`).  **The round hierarchy of block-radial energies has exactly three levels whenever such a
grouping exists**, and over all splits together.  For a class without one it has two: by Theorem H2 itself
`c_2 = h` when `min(φ₁, φ₂) ≥ 1 − h/a`, which two equal blocks satisfy as soon as `h/a ≥ ½` (`u ≳ 6.1`).

| `u` | `a` | `θ₂*` (two rounds, best split) | `h` (three rounds and more) |
|---|---|---|---|
| 0.5 | 0.03030 | 0.01059 | 0.00767 |
| 1 | 0.11094 | 0.03987 | 0.02914 |
| 2 | 0.32781 | 0.12918 | 0.09728 |
| 4 | 0.60305 | 0.29415 | 0.23925 |

(`θ₂*` at `u = 2, 4`: the reviewer's six-digit values `0.129184`, `0.294153`; our grid gave `0.12916`, `0.29417`.)

**Corollary H4 (barrier).**  Let a lower bound for `r ≥ 3` rounds be attempted by the method of Lemma 11.85:
twins `F_D, F_S` in some `BR_m`, regions `𝒲_1 ⊂ … ⊂ 𝒲_r` with `F_D = F_S` on `𝒲_r`, such that on `𝒲_t` the
functions depend only on the blocks whose centres the first `t` batches may know, and such that `𝒲_t`
contains what a batch of `e^{nθ}` points sees that knows the earlier centres.  If `θ > h`, `m` is fixed (more
generally `m·ln n = o(n)`) and all blocks have size at least `N_u`, then with `Θ = nθ − o(n)`

    |ln A(F_D) − ln A(F_S)| ≤ ln(1 + (n+1)^m e^{m(u+5L) − (Θ − nh)}) → 0 :

there is no gap.  (Apply Lemma B to `F_D` with `P` the blocks of level 1, `Q` those of level 2, `T` the rest:
every type outside `𝒲_r ⊃ V_{P∪Q}(Θ)` has mass at most `e^{−(Θ−nh)+m(u+5L)}` times a mass that the two functions
share; the other direction because `F_S = F_D` on the `𝒲_t`.)  This holds for every slope, every split,
every profile, and — because a group of blocks may play the role of `P`, `Q` or `T` — for every assignment
of blocks to rounds.
*Scope* (reviewer's finding M1).  This is a statement about applications of Lemma 11.85, in which every batch
is handed the centres — hence the blocks — of the earlier levels, and about boundedly many blocks.  With
one-coordinate blocks `BR_n = L_u`, and for `m ≳ n/ln n` the statement is empty: nothing here excludes a
hard three-round family living on that many blocks.  The reviewer also checked the deduction against the
lemma: its hypothesis `p_t ≤ e^{−nθ+o(n)}` forces `𝒲_t ⊇ V_{<t}(nθ − o(n))`, so (H1), (H2) hold for `r ≥ 3`.
Hidden partitions, which Lemma 11.85 does not model, are the subject of the addendum.

**Simulation** [N] (`experiments/phase2_hierarchy/h3_round_algorithms_sim.py`, output
`out/h3_round_algorithms_sim.txt`).  For a block-radial energy everything the algorithms R1 (plain Monte
Carlo), R2, R3 do depends on the sample only through the types, so they can be simulated exactly at the
level of types at realistic exponents (Poisson counts per type; `u = 2`).  Reported is `ln Â − ln A`, `A`
exact.

| instance | `ln M` | R1 | R2 | R3 |
|---|---|---|---|---|
| cone, blocks `(150,150)`, `nh = 29.2`, `na = 98.3` | `29.2` | `−35.8 … −31.3` | `0.000` | `0.000` |
| deep twin of Theorem 11.86, blocks `(720,480)`, designed against `Θ_c = 1.15nh = 134.2` | `110.2`–`126.2` | `−2.06 … −1.99` | `−0.51 … −0.44` (only block 1 revealed) | `0.000` |
| the same | `134.2`, `142.2` | `−1.98 … −1.86` | `0.000` (both revealed in round 1) | `0.000` |
| extremal function of Lemma B, blocks `(96,192,192)`, designed against `Θ_c = 0.70nh` | `Θ_c − 16`, `Θ_c − 8` | `−13.7 … −12.7` | `−13.2` | `−13.1 … −8.6` |
| the same, `Θ_c = 1.15nh` and `1.30nh` | `Θ_c − 16 … Θ_c + 8` | `−0.07 … +0.17` | `0.000` | `0.000` |
| four random admissible profiles, blocks `(100,100,100)` | `1.2nh` | up to `−2.3` | `0.000` | `0.000` |

Reading: below `h` nothing works (the hinted lower bound; third line from below); the two-round twin
defeats R2 and not R3; and the extremal function of the lemma, designed against a budget above `h`,
*hides nothing even from R1* at these sizes — which is the content of Lemma B.  An instance designed
against the budget `Θ_c` hides its structure from `M` points only if `ln M` is below `Θ_c` by a margin of
the order of the logarithm of the number of types; the sweeps show both sides of that margin.

---

## 7. Beyond disjoint blocks: two further obstructions

Lemma B is about centres that live in disjoint, known blocks.  The directive asked for attacks with
"distributed rather than concentrated hidden information" and for "pseudorandom families".  Two such
attacks were carried through.  Both fail, for reasons that are again relaxation arguments.

### 7.1 Overlapping centres: flags of hidden directions, any Lipschitz body (small-slope limit)

*The limit model.*  For a unit vector `v ∈ ℝⁿ` let `Y_v(x) = 2⟨x̃, v⟩/(u√n)`, `x̃ ∈ {±1}ⁿ`.  As `u → 0`, in units
of `a ≈ u²/8`: a uniform point has `Y_v ≥ y` with probability `e^{−na·y²(1+o(1))}` for spread-out `v`; an energy
`ψ = na·F(Y_{v₁}, …, Y_{v_r})` of orthonormal `v_j` is in `L_u` iff the gradient `Σ_j ∂_jF·v_j` lies in
`(2/√n)[−1,1]ⁿ`.  Let `K ⊂ ℝ^r` be the set of admissible gradients in the frame; `K` is a symmetric polytope
(a central section of a box) **contained in the Euclidean ball of radius 2**, touching the sphere exactly
in the directions of sign vectors.  Examples: block centres give the box `Π_j[−2σ_j, 2σ_j]`, `σ_j² = φ_j`;
`r` full-cube centres with prescribed overlaps — an energy `F(d(x, s¹), …, d(x, s^r))`, which is block-radial
only for the *hidden* partition of the coordinates into sign patterns — give other sections, e.g. the
cross-polytope `‖g‖₁ ≤ 2` for pairwise orthogonal centres.  In this model: types `Y ∈ ℝ^r`, rate `|Y|²`,
`F(Y) − F(e) ≤ h_K(Y − e) ≤ 2|Y − e|`, `h = ¼`, and a batch of `e^{nθ}` points that knows the directions
`e_1..e_{t−1}` of a *flag* sees `𝒲_t = {Σ_{j≥t} Y_j² ≤ θ}`; a revealed-centre argument needs `F` to depend on
`Y_{≤t}` only on `𝒲_t`.

> **Proposition G (flags).**  In the limit model let `r ≥ 3`, `θ ≥ ¼`, `K` any body inside the ball of radius
> 2, and let `F` be `K`-Lipschitz, depending only on `Y_{≤ r−2}` on `𝒲_{r−2}` and only on `Y_{≤ r−1}` on
> `𝒲_{r−1}`.  Then every type `Y*` with `|Y*_r| ≥ √θ` has mass exponent `−F(Y*) − |Y*|²` at most
> `M := sup_{𝒲_{r−2}} (−F − |·|²)`, and for `θ > ¼` at most `M − √θ(2√θ − 1)/4`.

*Proof.*  Write `Y = (p, q, w)`, `p = Y_{≤r−2}` with last coordinate `y`, `q = Y_{r−1}`, `w = Y_r`.  On
`D = {e : e_y² + e_q² ≤ θ, e_q² + e_w² ≤ θ}` the value `F(e)` is a value on `𝒲_{r−2}` (move `e_w`, then `e_q`, to
`0`), so `−F(e) ≤ M + |e_p|²`.  For `Y* = (p*, q*, w*)` with `y* ≥ 0` put `ρ = √(q*² + w*²) ≥ √θ`,
`b = √θ·|w*|/ρ ≥ θ/ρ`, and take the anchor `e` with the lower levels of `p*`, `e_y = min(y*, b)` and
`(e_q, e_w) = √θ(q*, w*)/ρ`; it lies in `D`.  Then

    −F(Y*) − |Y*|² − M ≤ e_y² + 2√((y* − e_y)² + (ρ − √θ)²) − y*² − ρ².

If `y* ≤ b` this is `2(ρ − √θ) − ρ² ≤ 1 − 2√θ ≤ 0`.  Otherwise put `Δ = y* − b > 0`; the right side is
`−[Δ² + 2bΔ + ρ² − 2√(Δ² + (ρ−√θ)²)]`, and the bracket is nondecreasing in `θ ∈ [¼, ρ²]` for fixed `ρ, Δ`
(with `b ≥ θ/ρ`), so it is at least `G₀(Δ, ρ) = Δ² + Δ/(2ρ) + ρ² − 2√(Δ² + (ρ − ½)²)`, `ρ ≥ ½`.  Now
`(Δ² + ρ² + Δ/(2ρ))² ≥ Δ⁴ + 2Δ²ρ² + ρ⁴ + 2Δ² + Δ²/(4ρ²)` (the cross term is `Δ³/ρ + Δρ ≥ 2Δ²`), so
`(Δ² + Δ/(2ρ) + ρ²)² − 4Δ² − 4(ρ − ½)² ≥ Δ⁴ + c₂Δ² + c₀` with `c₂ = 2ρ² − 2 + 1/(4ρ²)`,
`c₀ = (ρ−1)²(ρ² + 2ρ − 1) ≥ 0`.  For `ρ ≥ cos(π/8)`, `c₂ ≥ 0`; for `½ ≤ ρ ≤ cos(π/8)`,
`16ρ⁴(4c₀ − c₂²) = −(2ρ−1)³(16ρ³ − 8ρ² − 6ρ − 1) ≥ 0` because the cubic is negative there.  So `G₀ ≥ 0`.

*The margin for `θ > ¼`* (missing in the first version — equal exponents do not exclude a gap; the argument
is the reviewer's, finding M2, and was re-derived here).  Let `s = 2√θ ≥ 1`, `Δ = sΔ′`, `ρ = sρ′` (so `ρ′ ≥ ½`),
`R = √(Δ′² + (ρ′ − ½)²)`.  Substituting,

    Δ² + 2θΔ/ρ + ρ² − 2√(Δ² + (ρ − √θ)²) = s²·G₀(Δ′, ρ′) + 2s(s − 1)·R,

and both terms are nonnegative.  If `R ≥ 1/16` the second is at least `s(s−1)/8`; if `R < 1/16` then
`G₀(Δ′, ρ′) ≥ ρ′² − 2R ≥ ⅛` and the first is at least `s²/8`.  With `b ≥ θ/ρ` the bracket of the case `y* > b` is
therefore at least `s(s−1)/8 = √θ(2√θ − 1)/4`; the case `y* ≤ b` has the larger margin `2√θ − 1` (`θ ≤ 1`) or
`θ` (`θ > 1`).  ∎

The inequality `2√(Δ² + (ρ−½)²) ≤ Δ² + Δ/(2ρ) + ρ²` (`Δ ≥ 0`, `ρ ≥ ½`) is **machine-checked** [V]:
`proofs/Frontiers/FlagInequality.lean`, theorem `MetricChain.FlagInequality.flag_ineq` (with `cubic_nonpos`,
`quad_nonneg`, `flag_sq`; standard axioms only).  The reduction of the proposition to it is not formalised.

(`experiments/phase2_hierarchy/h4_flag_inequality.py`: the factorisation checked symbolically; `G₀ ≥ 0` on a
grid with minimum `0` at the plain dip `Δ = 0, ρ = 1` (it also vanishes at `Δ = ρ = ½`); for `θ > ¼` the minimum of the bracket is `2√θ − 1`,
so numerically the bound is the plain-dip value `1 − 2√θ`; a brute-force maximisation over hidden points
agrees within the anchor-grid error.)

*What this says.*  In the small-slope limit **no flag of hidden directions — blocks, overlapping centres,
hidden partitions — separates three or more rounds from `h`**, whatever the
Lipschitz body: the anchors that kill it lie in the region that the *penultimate* batch sees and where the
function still shows only what the batch before it revealed.  For two rounds the same model gives the
archive's value `0.346a` for every body (a cone at a vertex; the ball allows nothing more).  This is a
statement about a limit model, proved for scalar levels (with `y, q, w` replaced by norms and the anchor
taken radially the proof extends to levels of any dimension; not written out).  At finite slope the block
case is Lemma B; the general case was open when this was written and is now Theorem P of the addendum
for every structure that comes from a partition of the coordinates.

*Record of the attack that led here* (§9, F1): three full-cube centres with prescribed overlaps were tried
first as a way round the "smaller residual cube" — after the first centre is revealed the residual
problem keeps its full strength where the first structure has slope zero.  The necessary conditions for a
hidden cone at a vertex fail for all overlaps (`h6_failed_three_centres.py`, margins negative on every scan).

### 7.2 Exponentially many indistinguishable copies ("a code of cells")

*The idea.*  Let there be `N = e^{nR}` cells, each with its own hidden centres, all with the same profile,
`ψ = min_c F(type of x relative to cell c)`, and let one random cell carry the deep twin.  A batch that
knows the level-1 centres of all cells cannot choose the special cell: aligning with it costs
`min(r_P(z), R)` instead of `0`.  The later rounds stay diluted even though everything visible is known —
the "distributed" hidden information that the block chain lacks.

*The accounting* (exponents; `r_S(z) = Σ_{j∈S} φ_j f(z_j)`, `U = −F` per coordinate).  For a typical point the
number of cells of relative type `z` is `e^{n(R − r(z))₊}`.  Hence the visible mass exponent is
`m_vis = max_z [U(z) − (r(z) − R)₊]`, the special cell contributes `max_z [U_D(z) − r(z)]` (it has
multiplicity one), and a batch that knows the centres of the blocks in `S` of all cells reaches the type `z`
of the special cell at the cost `min(r_S(z), R) + r_{S^c}(z)` per point.

> **Proposition C (cells do not help).**  Let `θ ≥ h`, and let `F, F_D` be admissible with `F = F_D` on
> `𝒲₃ = {min(r_P + r_Q, R) + r_T ≤ θ}`, `F` depending only on `z_P` on `𝒲₁ = {r ≤ θ}` and only on `(z_P, z_Q)` on
> `𝒲₂ = {min(r_P, R) + r_Q + r_T ≤ θ}`.  Then `max_{z∉𝒲₃} [U_D(z) − r(z)] ≤ m_vis`, and for `θ > h`
> `max_{z∉𝒲₃} [U_D(z) − r(z)] ≤ m_vis − min{(θ−h)/4, h/2, u(κ−ζ)h/(2 ln 2)}`, where `ζ ∈ [p_u, κ)` is defined by
> `f(ζ) = min{a, h + (θ−h)/2}`.  **[P, at the level of exponents]**

*Proof.*  For `y ∉ 𝒲₃` (reflected so that `y_j ≤ ½`) take `e_j = max(y_j, κ)` on `P ∪ Q` and let `x = r_P(e) ≤ φ_P h`.
The cap is `U(e_P, ½, ½) ≤ m_vis + (x − R)₊`.
*If `x ≤ R`:* relax `T` to the rate `min(r_T(y), θ − x − r_Q(e))`; the anchor lies in `𝒲₂` with its `(P,Q)`-part
in `𝒲₁`, the cap is `m_vis`, and every block contributes at most `0` (relaxation to `κ` is free; `T`-blocks
relaxed deeper than `κ` contribute `≤ −(`rate`− h)`): `U_D(y) − r(y) ≤ m_vis`.
*If `x > R`:* relax `T` to the rate `min(r_T(y), θ − R − r_Q(e))` (at least `φ_T h`, because `R < x ≤ φ_P h`).  The cap
and the `P`-terms together give `x − R + Σ_P φ_j[u(e_j − y_j) − f(y_j)] ≤ φ_P h − R`, the `T`-terms at most
`−(θ − R − r_Q(e)) + φ_T h` or `−r_T(y) < −(θ − R)`; in both cases the total is at most `h − θ ≤ 0`.
*The margin for `θ > h`* (reviewer's finding M3: in the case `x ≤ R` with `T` not relaxed the bound above is
exactly `m_vis` for every `θ` — for instance at the cone point of a group of `P ∪ Q`-blocks of weight above
`θ/a` when `R > θ` — and equal exponents do not exclude a gap; the other sub-cases have the margin `θ − h`.
The repair is the reviewer's; it was re-read here step by step).  Let `δ = θ − h > 0`.  If `r_T(y) ≥ δ/4` the
bound of that case is `≤ m_vis − δ/4`.  Otherwise take the anchor `e′_j = max(y_j, ζ)` on `P ∪ Q`, `e′_T = y_T`.
Then `r(e′) ≤ h + δ/2 + δ/4 < θ`, so `e′ ∈ 𝒲₁` and `U_D(e′) = U(e′_P, ½, ½) ≤ m_vis + (r_P(e′) − R)₊`; and
`R < r_P(e′) ≤ h + δ/2` is impossible, because `y ∉ 𝒲₃` would then force `r_T(y) > θ − R > δ/2`.  So the cap is
`m_vis` and, with `u(ζ − y_j) − f(y_j) = −k(y_j) − u(κ − ζ)`,

    U_D(y) − r(y) ≤ m_vis − r_T(y) − Σ_{P∪Q: y_j ≥ ζ} φ_j f(y_j) − Σ_{P∪Q: y_j < ζ} φ_j [k(y_j) + u(κ − ζ)].

Since `r(y) > θ` and `r_T(y) < δ/4`, the `P ∪ Q`-blocks carry a rate above `h`: either the first sum is at least
`h/2`, or the blocks with `y_j < ζ` have weight at least `h/(2 ln 2)`.  ∎

So the dilution `R` of the later rounds is paid back by the multiplicity `R` that the special cell must
outweigh.  (The reviewer's own grid computation at finite slope, 432 parameter sets: the true hidden gain
of the cell model is at most the plain-dip value `D(θ) = u f^{−1}(θ) − Λ₁ ≤ h − θ` plus one grid step.)  [N]: `h5_cells_small_slope.py` (exact min-plus envelopes on a grid, box body, small-slope
limit): over 252 parameter sets the largest hidden gain equals the plain-dip value `1 − 2√θ` up to the
rounding of the regions to the grid (`+0.003` at `θ = 0.25`; `−0.015` against `−0.020` at `0.26`; `−0.055`
against `−0.058` at `0.28`).  At finite slope with exact binomial costs (`h8_cells_finite_slope.py`,
`u = 1, 2`, three splits, `R/h ∈ {0, 0.1, 0.3, 0.6, 1.2}`): the largest hidden gain is negative in all 30
cases at `θ = 1.2h` and `1.5h`, at most `+1.44` nats at `θ = h`, and positive (a hidden plain dip, as it must
be) at `θ = 0.7h`.  Codes at several levels (a tree of cells) were not written out; the same two-case
computation applies level by level.

### 7.3 Hidden partitions and overlapping centres at finite slope (addendum)

When this report was first written, the finite-slope version of §7.1 was open: Lemma B's anchor clips the
block distances one by one, and for a *merged* block — two hidden classes of which the batches control
only the sum — that anchor is not visible to the first batch as soon as the deep class is more than half
of the block.  The remedy is one more move: after clipping, raise the lowest classes of every deep cell
until the cell mean reaches the hinted radius; this move is aligned, so its Lipschitz cost is that of the
mean, and it does not increase the within-cell cost.  With it the argument works for arbitrary nested
partitions of hidden classes, with a per-cell price inequality that replaces (R).  Statement, proof,
algorithm and checks: `HIERARCHY_ADDENDUM.md` (Theorem P, Theorem H6).  Two probes made before the theorem
was found are kept there as checks: three overlapping centres at finite slope (`h10`), and the two-round
game with the hidden group split in two (`h9`: the two-block value is not exceeded beyond grid error,
supporting `c_2(BR_m) ≤ θ₂*`).

---

## 8. What remains open, and a conjecture

> **Conjecture H5 [C].**  `c_3(u) = h(u)` for every `u > 0`: on all of `L_u` three rounds of adaptivity reach
> the optimal exponent, and two do not.

*Evidence.*  Theorem H1 (every block-radial class, every slope) and Theorem H6 of the addendum (every
energy with a bounded hidden symmetry type; the algorithm is told nothing but the bound); Corollary H4
and Propositions G, C (every hard family of bounded structure that the known technique can analyse stops
separating at three rounds, for a structural reason: the relaxed image of a hidden type is visible one round earlier and is
Lipschitz-close); the inequality behind H6 (Theorem P) does not depend on the number of classes;
consistency with `c_1 = a`, `c_2 > h`, `c_∞ = h`.  *Against:* the algorithms sample the shells of a partition
with boundedly many cells, and their two hypotheses — each batch saw nothing finer than what it learned —
are exact consequences of a hidden symmetry.  An arbitrary member of `L_u` has no symmetry.  The only
universal upper bounds remain those of the nested algorithms (`T^{(3)}(0) = 0.541a`,
`T^{(r)}(0) − h ≈ 0.36a/(log₂ r)^p`), which never use slopes.

**Precise open problems.**
1. *Hidden partition.*  Is `c_3 = h` on the union of the classes `BR_m` over all partitions into at most `m`
   blocks?  **Settled: yes** (addendum, Theorem H6 with `HP_{2m}`), also when the profile couples blocks.
2. *Multi-centre energies* `F(d(x, s¹), …, d(x, s^m))` with overlapping centres.  **Settled: `c_3 = h`** for
   every fixed number of centres (addendum, `HP_{2^m}`).  Open in both problems: a number of classes that
   grows faster than `(n/log n)^{1/5}`.
3. *A universal certificate.*  For an arbitrary `ψ ∈ L_u` and a deep point `y`, the relaxation of `y` is the
   point obtained by re-randomising coordinates; Lemma B says its value was seen and is Lipschitz-close
   *because a round knew along which coordinates not to relax*.  Is there a three-round sampling scheme
   (gradient patterns pooled over the sample) and an inequality "for every `ψ ∈ L_u`: what the scheme has
   not sampled has mass at most `e^{n(h−θ)}` times what it has" ?  This would be the theorem.
4. *Two rounds on `L_u`.*  `c_2(u) ∈ [θ₂*, T^{(2)}(0)] = [0.359a, 0.624a]` at `u = 1`.  Theorem H2 shows that
   the lower end is attained on two blocks by an algorithm that reads centres off slopes.  Conjecture:
   `c_2(u) = θ₂*(u)`.  Also open: `c_2(BR_m)` for `m ≥ 3` (§5).
5. *A refutation of H5* would need a hard family with all of: (a) no bounded hidden symmetry type — not
   finitely many centres, blocks or classes in any arrangement (Theorem H6); (b) hidden information that
   is not merely replicated (Proposition C); (c) a hidden type whose relaxation to the hinted radius is
   invisible to the penultimate batch although its cost there is below the budget.  We do not know such
   a family.
6. *Rate over all algorithms* (priority 4).  On block-radial classes the question disappears (collapse at
   three).  On `L_u` the laws `1/k²` (levels) and `(log r)^{−p}` (rounds) are properties of nested
   algorithms; if H5 holds they say nothing about the problem.
7. *Beyond the cube* (priority 5).  The proof of Lemma B uses, per block: a cost `t` of the radius that is
   convex, symmetric under reflection and unimodal, with jumps of at most `L` and `t = O(L)` at the
   near-typical radii of both parities; the linear price `u` of a step; `γ = t + u·`radius `≥ nΛ − L`; and
   `γ(e) ≤ γ(y) + t(κn) + O(L)` for `y ≤ e ≤ κn`, `κ = Λ/u`.  It should therefore carry over to products of
   identical blocks with any reference whose radial costs have these properties (not checked).  Theorem P
   of the addendum uses even less: a convex rate per class and the function `χ` built from it.  For blocks of different kinds (several slopes, a field) the hinted
   anchor trades rate between blocks and the per-block argument must be replaced; not done.

---

## 9. Failed attacks (preserved)

F1. **Three overlapping centres** (energies of the distances to three hidden points with prescribed
 pairwise distances; the hidden information is "distributed": revealing the first centre does not shrink
 the residual cube).  Small-slope model, cone at a vertex, exact envelopes in the plane of the first two
 centres.  Every scan negative; the binding anchors are those of Proposition G.  `h6_failed_three_centres.py`.
F2. **A first, wrong, accounting of cells.**  The mass cap was taken per cell (`U ≤ r`) and the multiplicity
 subtracted afterwards; this double-counts at types that are typical for many cells (there `min_c` already
 lowers the landscape by `R`).  Correct cap: `U ≤ m_vis + (r − R)₊`.  With the wrong cap the cells looked
 strictly harmful, with the right one exactly neutral.  The check "the game with unboundedly many rounds
 must give at most `h`" caught a related slip (a composite of an outer code and inner dips that seemed to
 cost `0.31a > h`: the inner dip leaks to blind points through the Lipschitz coupling).
F3. **Round elimination** by planting an `(r−1)`-round instance in the fibres over a code: the first round is
 not eliminated — a blind batch gives every cell a full-budget blind sample, because one point serves all
 cells — and the planted instance must then be hard for `r` rounds at a *lower* budget, which is circular
 except below `h`.
F4. **Finite-slope three-block chain**, caps only (`u = 0.5, 2, 4`): negative for every split tried; now a
 special case of Lemma B.
F5. **A universal three-round algorithm** (follow pooled gradient patterns; certify by Lipschitz anchors):
 no certification inequality found for arbitrary `ψ`; this is open problem 3.
F6. **Class-wise clipping for hidden partitions** (the first attempt at open problems 1 and 2): write the
 lemma for classes instead of blocks and clip every class density towards `½` at the hinted radius.  For a
 merged block the anchor's blind cost exceeds what the hidden part earns (`P(e) > T(e)`) as soon as the deep
 class is more than half of the block — in the small-slope limit `P = θ·w/(1−w)` — so the first free step
 is not available.  Contracting the deviations towards the cell means (the anchor of Proposition G) moves
 classes *away* from `½` and its price is not controlled by (R) at finite slope.  What works is in between:
 clip, then fill the deep cells from below (addendum §A2).
F7. **A sharper numerical claim than the lemma** ("no logarithmic loss at `θ ≥ 1.1h`"), read off 124 cases:
 false on other splits (§3, corrections).  The cases had been chosen by the author of the lemma.

---

## 10. Significance, closest prior art, publication assessment

**What is new relative to the archive.**  Lemma B (finite `n`, explicit constants); Theorem H1 for every `m`
and every slope with a complete proof for `n ≥ n₀(u, m, η, ε, δ)`, `n₀` not explicit (the archive: a sketch for
two blocks, U10(b), and a numerical failure of one three-block family in the small-slope limit); the matching upper bound of Theorem H2 (the archive: a conjecture with
its key step numerical); the barrier H4; Propositions G and C; and, in the addendum, Theorem P (the
relaxation principle for nested hidden partitions) and Theorem H6 (three rounds suffice on every class of
bounded hidden symmetry type, with an algorithm that is not told the structure).

**What it means.**  On every class `HP_m`, `m ≥ 4`, of energies with a bounded hidden symmetry type the
hierarchy is `a > c_2 > h = h = …`: *exactly three levels*, with `c_2 ≥ θ₂*(u)` (the best two-block split; for
a single block-radial class with fixed block fractions the middle level can coincide with `h`, §6).  The archive's
statement "the particular hierarchy of nested algorithms approaches `h` with a sharp `1/k²` law" is about an
algorithm; an algorithm that reads the hidden structure off local slopes reaches `h` in three rounds.  The
question for all Lipschitz energies is now a clean alternative (Conjecture H5 against a family as in
open problem 5), and the second branch is narrow: every construction with finitely many hidden objects
is excluded.

**Closest prior art** (from the archive's sweeps and three searches of ours on 2026-11-28; *search-engine
summaries only, no paper read*):
* *Limited adaptivity in partition-function estimation with a sampling oracle.*  For Gibbs distributions
  with sample access at chosen temperatures, non-adaptive schedules are provably worse than adaptive ones,
  and recent work reports near-optimal sample complexity with **two or three rounds** of adaptivity
  (arXiv 2505.18324, "Simple parallel estimation of the partition ratio for Gibbs distributions"; arXiv
  2604.01263; arXiv 2609.20337 for a non-adaptive lower bound).  Different oracle (samples, not
  evaluations), different class, polynomial rather than exponential scales — but the same phenomenon, a
  collapse after a small constant number of rounds, and the closest thing we found.
* *Round hierarchies that do not collapse:* Canonne–Gur (property testing: a strict hierarchy at every
  level), Agarwal et al. (top-`k` coins: `Θ(log* n)` rounds), Brânzei–Li (local search in rounds: a
  different exponent for every constant number of rounds), parallel convex optimisation (Nemirovski;
  Balkanski–Singer; Bubeck et al.; Diakonikolas–Guzmán), sparse recovery (Price–Woodruff).
* *Information-based complexity:* adaption against non-adaption (Novak's survey; Heinrich); no count of
  adaptive stages found.
"Not found" is not "new"; a specialist in information-based complexity or in parallel sampling may know a
three-stage result of this kind.

**Publication assessment.**  (i) As a section of the candidate mathematics paper of the programme (adaptive
query complexity of a certified free energy), Theorems H6 (with H1 as its explicit special case), H2 and
Theorem 11.86 make the treatment of rounds complete on all energies of bounded hidden symmetry type and
replace an open-ended "two rounds are strictly between; three: unknown" by a theorem and a sharp
conjecture.  That is a real strengthening of that paper.  (ii) As a standalone note — "three rounds of
adaptivity are necessary and sufficient for certifying a free energy with hidden symmetry" — it has a
complete statement on a natural class (invariance under an unknown Young subgroup), a matching
two-round lower bound from the archive, a short central inequality (Theorem P), and an honest open
problem (no symmetry).  Its weight still depends on Conjecture H5, but less than before: the class is no
longer a model class chosen to fit the lower-bound constructions.  (iii) Before any submission: an
external human reading of §§3–5 and of the addendum §A2, §A4 (Theorem H6 is a paper proof found on the last
day; its review is recorded in §12 and in the addendum §A6); the dependence on the archive's Theorems
11.25, 11.44/45 and 11.86 (paper proofs for the upper bounds, refereed internally only); a literature
check by a specialist — partition learning from slopes is close in spirit to learning juntas and
symmetric structure from queries, and we have not searched that literature.  We do not claim the general
problem solved.

---

## 11. Reproducibility

All scripts are in `experiments/phase2_hierarchy/`, outputs in `out/`; Python 3 with numpy, scipy, sympy;
run from that directory; one process, the 4-core container, no external computation.

| script | what | time | output |
|---|---|---|---|
| `h1_relaxation_lemma_check.py` | Lemma B on its extremal functions, 124 cases, exact binomials | 40 s | `out/h1_relaxation_lemma_check.txt` |
| `h2_two_round_verify.py all` | priority 1: thresholds `θ₂*(u)`; exact twins; gap against the formula | 2 min | `out/h2_two_round_verify.txt` |
| `h3_round_algorithms_sim.py` | type-level simulation of R1, R2, R3 | 40 s | `out/h3_round_algorithms_sim.txt` |
| `h4_flag_inequality.py` | Proposition G: factorisation, grids, brute force | 7 min | `out/h4_flag_inequality.txt` |
| `h5_run.py` (uses `h5_cells_small_slope.py`) | Proposition C: the cell game on a grid | 3 min | `out/h5_cells_small_slope.txt` |
| `h6_failed_three_centres.py <π₁ π₂ π₃ π₄ θ>` | record of failed attack F1 | seconds per case | — |
| `h7_r3_on_cubes.py` | Algorithm R3 literally on cubes `Q_12`–`Q_14`, with two mutations | 80 s | `out/h7_r3_on_cubes.txt` |
| `h8_cells_finite_slope.py` | Proposition C at finite slope, exact binomials | 12 s | `out/h8_cells_finite_slope.txt` |
| `h9` – `h12` | checks of the addendum (two rounds with a split group; three centres at finite slope; Theorem P; Algorithm R3P on cubes) | see addendum §A7 | `out/h9_*` … `out/h12_*` |

Lean: `lake build proofs.Frontiers.TwoRounds proofs.Frontiers.TwoRoundsExpected` (pinned toolchain, Mathlib
cache) — built here, 8559 jobs, no error.  This division's Lean files: `proofs/Frontiers/RelaxationCore.lean`
(six theorems), `proofs/Frontiers/FlagInequality.lean` (four), `proofs/Frontiers/PartitionChain.lean` (four);
each compiles without warnings with `lake env lean <file>`; axioms `propext`, `Classical.choice`,
`Quot.sound` only.

---

## 12. Reviews and independent replication

Everything in this section was done by AI sessions.

**(1) Adversarial review of this report** (`HIERARCHY_REVIEW.md`; scripts and outputs in
`experiments/phase2_hierarchy/review/`).  A second session with its own code reviewed the report as it stood
at 02:43 UTC (before the additions of this version and before the addendum).  *Verdict: no critical
finding; Lemma B, Theorem H1, Lemma A2 and Theorem H2 survived the paper check and every numerical attack*
(facts (F1)–(F4), (R) exactly, 0 violations; Lemma B on about 6 000 exact extremal functions with
parity-dependent profiles, inside the lemma's hypothesis, `m = 2…5`, `n` up to 4000: largest excess `+0.89`
nats against allowances of 36–146, not growing with `n`; Algorithm R3 literally on cubes with `n ≤ 20`;
Lemma A2 on 168 exact extremal cases, the hidden gain changing sign at `ϑ(φ₁)`).  Three major findings,
all applied above:
 * M1 — the barrier was announced for "any number of blocks"; it needs boundedly many blocks of size at
   least `N_u` and concerns applications of Lemma 11.85 (§0, Corollary H4).
 * M2 — Proposition G gave only "`≤ M`"; the margin for `θ > ¼` was supplied by the reviewer (§7.1).
 * M3 — Proposition C had one sub-case without a margin; repaired by the reviewer with a second anchor (§7.2).
Nine minor findings (hypothesis `n_j ≥ N_u` missing in §0; "exactly three levels" false for some fixed
classes; the cases of §3 outside the lemma's hypothesis and without parity; two fifth digits in the table
of §6; a deterministic *bound* on the cost; "`→ 0`" for "`O(log n)`" in H4; the list of ingredients in §8.7;
"finite-`n`" for H1; the origin of the lower bound in §5): all applied.  *Not covered by that review:*
the archive's theorems used here (11.25, 11.44/45, the proof of 11.86), §2, §9, the prior-art paragraph,
the modelling steps of §7, the simulation of §6 (read, not re-run), and everything added later — the
corrections of §3, §7.3, the Lean files, `h7`–`h12`, the addendum.

**(2) Independent replication by the engineering division** (`ENG-RES-0020` on
`research/phase2-certified-inference`; code written from this report, not from our scripts; predictions
written before the runs).  Lemma B: criterion holds in 220 of 220 cases; our sharper numerical remark does
not (§3, corrections).  Algorithm R3: properties (a)–(c) without exception on 32 instances, mutation caught
(§4).

**(3) Review of the addendum**: see `HIERARCHY_ADDENDUM.md` §A6.
