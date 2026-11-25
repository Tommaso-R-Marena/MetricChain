# Workstream U — rounds of adaptivity: what does a bounded number of rounds cost?

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs by one author, refereed after integration (Scientific
> Discovery Division, SCI-REV-0003: no critical finding, one major, nine minor — see the
> errata below); before that checked and re-computed in
> part by the coordinator** — Theorem U1 line by line against the proof of Theorem 11.56
> (`docs/workstreams/K_REPORT.md` §2), Lemma U2 (re-derived; the coupling is stated in the theory
> report through a "virtual run", which avoids conditioning on the events `E_t`), Theorem U3
> (re-derived; the asymptotic formula, `θ₂*` at five slopes, and the exact finite-`n` twins
> re-computed with an own implementation from the statement), the two- and three-round values
> of the recursion (`experiments/coordinator_checks/rounds_U/`; no discrepancy).  Not re-computed:
> the recursion beyond three rounds, §2.4, §3.3.  The integrated statements and their labels are
> in `docs/THEORY_REPORT.md` §11.24: Theorem U1 and Corollaries U1.1–U1.3 = Theorem 11.84, Lemma U2
> = Lemma 11.85, Theorem U3 = Theorem 11.86, Corollary U4 = Corollary 11.87, Propositions U6, U7,
> U9, U10 and §3.3 = Proposition 11.88.  Lemma U2 for two rounds was machine-checked by the
> coordinator after delivery (`proofs/Frontiers/TwoRounds.lean`; the report's "no Lean" refers to
> its own work).  Harness: block XX and DEAD.21 of
> `experiments/falsify_conjectures.py`.  The author's scripts and outputs are in
> `experiments/workstreams/U/` (`code/`, `out/`; the report's `scratchpad/ws/U/` is that directory).
> The coordinator's observations (i)–(iii) that the report comments on are in
> `docs/workstreams/U_brief.md`; (iii) — nested basins — was wrong (`docs/DEAD_ENDS.md` D50).

> **Errata after the review SCI-REV-0003** (Scientific Discovery Division, branch
> `research/scientific-translation`, `docs/science/workstreams/R4_REPORT.md`: an independent
> review with own code; no critical finding, one major, nine minor; the two-round lower bound
> "proved", Theorem U1 "proved" once its stopping rule stands before the stage).  The text
> below is unchanged; the following points of it are corrected in the theory report §11.24.
> **(M1) Theorem U1(i), "at most `C_B` evaluations in every run", is not proved by the text as
> written.**  Claim B bounds `|C_l|` under its proviso only ("otherwise B2L⁺ has stopped"),
> and the rule "a stored bracket of rung `l−1` has ratio above `e^{x_{l−1}}` → trivial bracket"
> is listed under *Output* (§1.2), that is after the evaluations it is meant to prevent.
> If the brackets of rung `l−1` are wider than promised — an inner procedure may return its
> trivial bracket with probability `δ′` — then `C_l` can be all of `C_{l−1}` (the division's
> run: `|C_2| = 393 216 = M_max` against `N_2 = 79 931`).  Read: "*before stage `l`*: if
> `|C_l| > N_l` (or if a stored bracket of rung `l−1` has ratio above `e^{x_{l−1}}`), stop and
> return the trivial bracket".  On `𝒢′` the rule never fires, so (ii) is unchanged, and (i)
> then holds in every run; no exponent changes.  (m7) Proof of Claim B, "`M* = K` is
> impossible here (it would force `i ≤ 2ν s_j/(λ_je^b) < K/2`)": the reason is
> `K < i ≤ min{M_max, 2ν s_j/(λ_je^b)}`, whence `M* ≥ 2K`; the conclusion stands.  (m1) The
> sentence that closes §1.2 ("every exponent statement derived from Theorem 11.56 … holds
> for the batched algorithm") is true for a fixed choice of the levels; for Theorems 11.54
> and 11.58 it gives `h + 3η` with `r(η)` rounds (Corollary U1.3), not the exponent itself with
> a fixed number of rounds.  (m3) Lemma U2: "batch sizes at most `M_t`" is needed, and to be
> read, for the runs on the instances `ψ_s` only; and for two rounds no bound is needed at
> all: the division's Theorem R4.1 (machine-checked; `proofs/Frontiers/TwoRoundsExpected.lean`) gives
> `1 − 2δ ≤ E|B₁|·p₁ + E|B₂|·p₂` with the second batch taken on the flat histogram of the first
> block, a member of the class, so the two-round bound of Theorem U3 holds for the expected
> cost at that instance, and the Markov remark of the notation paragraph and of §8 is
> superseded.  (m4) "A third batch can" (§0) and "A third round reads it off" (§2.3) are the
> **[sketch]** of Proposition U10(b), for an algorithm that knows the two blocks; for
> algorithms correct on `L_u` three rounds are only known to cost at most
> `T^{(3)}(0) = 0.541a`.  (m5) The finite-`n` sentences of §0 and §2.2 ("two rounds need
> `e^{0.0382n}` evaluations, the hinted lower bound is `e^{0.0294n}`") compare two lower
> bounds; no separation from adaptive algorithms is shown at any finite size.  (m9) The
> values `T^{(r)}(0)` for `r ≥ 4`, and with them "`τ^{(48)} < τ^{(2)}`" (Corollary U4(c)), have no
> stored witness: `out/ub_rounds_*.txt` keeps the value and one parameter for each `r`, not
> the ladders and the allocation of rounds.  Not errata of this report: m2 and m6 (the
> restriction `r_l ≤ r − 1` and the `limsup`/`liminf` convention are here and were lost in the
> theory report) and m8 (about the Lean file).

Independent report.  Directory `scratchpad/ws/U/` (this file, `code/`, `out/`); nothing in the repository was
modified, no state-changing git command was run, nothing was delegated.  The repository was read at commit `caf1dc5`
(later than `36613b9`), in the first hour of the work; its working tree was being edited by others later on
(`docs/THEORY_REPORT.md` among the files), and those edits are not reflected here.  All numerics are own code (numpy/scipy), fixed seeds, `ulimit -v 4000000`, every run under
ten minutes, one heavy process at a time; commands, sizes and run times are in §9.

Status labels: **[proved]** complete proof in this report (a paper proof by one author, unrefereed; where it rests on
a theorem of the theory report or on a finite computation this is said); **[sketch]** missing steps named;
**[numerical]**; **[conjecture]**; **[known]** (source, and how much of it I read).

Notation (theory report §§11.16–11.19): `Q_n`, `L_u`, `w = e^{-ψ}`, `A = 2^{-n}Σ_x w(x)`; `p_u = 1/(1+e^u)`,
`Λ₁ = ln(2/(1+e^{-u}))`, `f(ρ) = KL(ρ‖½)`, `k(ρ) = KL(ρ‖p_u) = f(ρ) + uρ − Λ₁`, `a = f(p_u)`, `h = f(Λ₁/u)`,
`ε* = ln cosh(u/2)`; `θ_na(e) = min{f(ρ) : k(ρ) ≤ e}`, `θ_hint(e) = f((Λ₁+e)/u)`.  Two inverse functions are used
throughout:

    D(θ)    = u·f^{-1}(θ) − Λ₁          (accuracy rate certified by e^{nθ} evaluations with a hint; D(h) = 0, D ↓)
    x_na(θ) = D(θ) + θ = k(f^{-1}(θ))   (the same for a non-adaptive sample: the shear law of §11.21),

`f^{-1}` being the inverse of `f` on `[0, ½]`.  An *r-round algorithm* asks `r` batches `B₁, …, B_r`, each chosen after
the answers to the earlier ones; its cost is the total number of evaluations.  Upper bounds below are worst-case
bounds over `L_u` that hold for every run; lower bounds are for `max_t |B_t|` (hence for the total), for algorithms
with deterministic batch sizes, and extend to expected batch sizes by Markov's inequality at the price of a constant.
`τ^{(r)}` is the exponent of the least cost at a bounded accuracy; "`τ^{(r)} ≤ X`" is a statement about `limsup`,
"`τ^{(r)} ≥ X`" about `liminf`.  `τ^{(1)} = a` and `τ^{(∞)} = h` are Theorems 11.44/11.45 and 11.58 **[known]**.

---

## 0. Verdicts

| question | verdict | label |
|---|---|---|
| Q1: is `τ^{(2)} < a`? | **Yes.**  `τ^{(2)} ≤ T^{(2)}(0) = min_{φ,ξ} max{φa + (1−φ)θ_na(ξ), min(φa,(1−φ)ξ) + (1−φ)a}` — two levels, two rungs, one rung per round.  `T^{(2)}(0)/a = 0.618` (`= (√5−1)/2`) in the small-slope limit, `0.624` at `u = 1`. | [proved, given Theorem 11.56 (K1) and Proposition 11.57(b)]; Theorem U1, Corollary U1.2 |
| Q1: is `τ^{(2)} > h`? | **Yes, for every `u`.**  `τ^{(2)} ≥ θ₂*(u) > h`, with `θ₂*/a = 0.346, 0.359, 0.394` and `θ₂*/h = 1.38, 1.37, 1.33` at `u → 0, 1, 2`.  Family: two blocks of coordinates, a "flat histogram" in the first, a hidden dip in the second whose size follows what a blind batch can see shell by shell.  Exact at finite `n`: at `u = 1`, `ε = 1`, `n = 12 800` two rounds need `e^{0.0382n}` evaluations, the hinted lower bound is `e^{0.0294n}`. | [proved]; Lemma U2, Theorem U3; exact computations `lb2_exact.py` |
| Q2: is `τ^{(r)}` strictly decreasing? | `a = τ^{(1)} > τ^{(2)} > h = lim_r τ^{(r)}`, so the sequence takes at least three values; `τ^{(48)} < τ^{(2)}` at `u = 1`.  Strict decrease at every step: **open**.  For `r ≥ 3` the only lower bound I have is `h`: the natural three-block continuation of the two-round family hides nothing at budget `e^{nh}`. | [proved] / [numerical] for the last sentence (§2.4) |
| Q2: does `τ^{(r)} → h`, at what rate? | **Yes.**  The nested algorithms of §§11.18–11.19 need a number of rounds that does not depend on `n` once the ladders are processed rung by rung (Theorem U1): a ladder with `L` rungs is `L` rounds, `k` levels with `L` rungs each are `L^{k−1}` rounds.  Computed upper bounds `T^{(r)}(0)/a = 0.625, 0.541, 0.481, 0.454, 0.440, 0.421, 0.394, 0.379, 0.364, 0.354, 0.342, 0.335` for `r = 2, 3, 4, 5, 6, 8, 12, 16, 24, 32, 48, 64` at `u = 1` (`h/a = 0.263`): `(T^{(r)}(0) − h)/a ≈ 0.36/(log₂ r)^p` with `p` rising from `0.75` to `0.9` over this range.  No lower bound on the rate. | [proved] convergence; [numerical] values and rate |
| Q2: relation to the level values `τ_k`; rounds of Algorithm 2L⁺ | As written, 2L⁺ uses up to `(J+1)(m_max+1)·L = Θ(n²L)` rounds (levels × doublings × rungs).  Batched: exactly `L` (times the rounds of the inner procedures).  `τ^{(L^{k−1})} ≤ τ_k^{[L]}`, the `k`-level exponent with `L`-rung ladders, which decreases to `τ_k` as `L → ∞`; e.g. `τ^{(4)} ≤ 0.481a < τ₂ = 0.5006a`.  A coarse ladder costs what Proposition 11.57(b) says: `max_l [min(φa,(1−φ)ξ_{l−1}) + (1−φ)T(ξ_l)]`.  No lower bound of the form `τ_k`. | [proved] |
| Q3: what a round can do | (a) Conditional covering: a ball of radius `κn` whose centre is at distance `σn` from a known point costs `exp(n(f(κ) − f(σ))₊)` to hit, and no less.  (b) A dip that sticks out of a plateau ball is seen from the antipode of the plateau's centre with one evaluation, so nested balls hide only what they contain.  (c) On block-radial classes the cost of `r` rounds *is* a variational problem on the space of types (the "type game"): a batch that knows the centres of the blocks in `S` sees exactly the types whose unknown part has rate at most the budget; for two blocks its value is `a` for `r = 1`, at least `θ₂*`-type bounds (conjecturally equal) for `r = 2`, and `h` for `r ≥ 3`.  For all of `L_u` there is the recursion `T^{(r)}` from above and `θ₂*` from below, nothing sharper. | (a), (b) [proved]; (c) lower bounds [proved], upper bounds [sketch] |
| Q4: radial instances | Exactly two rounds: `τ^{(1)}(R_u) = a`, `τ^{(2)}(R_u) = h`. | [proved from Theorem 11.51 [known]]; own run on `Q_14` |
| Q4: a class between radial and `L_u` | Block-radial functions `ψ = F(d(x¹,s¹), d(x²,s²))` (two known blocks; contains `R_u`): two rounds do **not** suffice for `h` (`τ^{(2)} ≥ θ₂*(φ₁) > h`), three do. | [proved] / [sketch] |

**The coordinator's observations.**  (i) is right (a cone is determined by one point and its `n` neighbours, Theorem
11.45(d)); (ii) is right; (iii) points in the wrong direction.  Nested basins with hidden centres do *not* separate
two rounds from many in the families I could analyse (§3.3): a basin that matters is wide, a blind batch of `e^{nh}`
points lands on every level that is cheap, and what remains hidden costs at most `e^{nh}` again.  The separation that
exists comes from **dilution**: a visible structure in one block that makes every shell equally heavy forces the first
batch to spread over the shells; on each shell it then sees too little of the second block to notice a dip there, and
the second batch — which knows the first centre and can look at every shell with full strength — sees the rim of the
dip but cannot reach its bulk.  A third batch can.

**What is conjectural or open** is collected in §8.

---

## 1. How many rounds the existing algorithms use, and Theorem U1

### 1.1 Algorithm 2L⁺ as written

In `K_REPORT.md` §2.2 the inner procedures are called inside three nested loops: levels `j = 0..J`
(`J = ⌈(2un + b + n_o ln 2)/λ⌉ = Θ(n)`), sample sizes `M = K, 2K, …, K2^{m_max}` (`m_max = Θ(n)`), and, for each point
of a pass, rungs `l = 1..L`.  The points of one pass can be refined in parallel, rung by rung, but the sample size of
level `j` depends on the running bound `ℓ`, which depends on the classifications at the levels below.  A direct
implementation therefore uses up to `(J+1)(m_max+1)·Σ_l r_l` rounds, `r_l` the number of rounds of the inner procedure of
rung `l` — `Θ(n²L)` for one level over one-round brackets, and the product of such factors for nested levels.  That the
number of rounds grows with `n` is a property of the *schedule*, not of the algorithm:

### 1.2 Theorem U1 (a ladder is as many rounds as it has rungs)

Setting and notation of Theorem 11.56 = Theorem K1 (`K_REPORT.md` §§2.1–2.4): outer points `a₁, a₂, …`, levels
`s_j = s₀e^{jλ}`, inner accuracies `2un_i = x₀ > x₁ > … > x_L`, `x_L ≤ b`, inner procedures `I_1..I_L` with costs `C_l`,
constants `J, ν₀, ν = Kν₀, m_max, M̄, c_η = (1−η)/(1+η)`, initial bound `ℓ₀ = e^{-ψ₀}((1+e^{-u})/2)^n`, doubling sequence
`ℳ = {K2^m : 0 ≤ m ≤ m_max}`, `M_max = K2^{m_max} < 2M̄`.  As in the proof of K1 every *potential* inner call
`(i, l)` has its own randomness, drawn in advance.

**Algorithm B2L⁺ (batched).**
* *Stage 1.*  Ask `ψ(0ⁿ)` and `ψ(a_i, 0)` for all `i ≤ M_max` (the reference point and the trivial brackets) together
  with the first batch of `I_1` on the fibres of **all** `a_i`, `i ≤ M_max`; finish `I_1` on all of them in parallel.
  Put `C_1 = {1, …, M_max}`.
* *Stage `l = 2, …, L`.*  Let `[L_i, U_i]`, `i ∈ C_{l−1}`, be the stored brackets (intersections of rungs `0..l−1`).
  For `j ≤ J`, `M ∈ ℳ` put `N_L(j, M) = #{i ≤ M, i ∈ C_{l−1} : L_i > s_j}`,

      λ_j  = max{ ℓ₀ ,  c_η(1+η)^{-1}e^{-b} · max{ s_{i'}·N_L(i', M)/M  :  i' < j, M ∈ ℳ, N_L(i', M) ≥ K } },
      M̂_j = max{ K , 2ν s_j/(λ_j e^b) },
      C_l  = { i ∈ C_{l−1} : there is j ≤ J with  i ≤ M̂_j ,  U_i > s_j ,  L_i ≤ s_j e^{-b} },

  and run `I_l` on the fibres of all `a_i`, `i ∈ C_l`, in parallel.
* *Output.*  Run Algorithm 2L⁺ as a computation on the stored brackets (a call `(i, l)` is answered by the stored
  result).  If it asks for a pair with `i ∉ C_l`, or a stored bracket of rung `l−1` has ratio above `e^{x_{l−1}}`, return
  the trivial bracket `[s₀, s₀e^{2un}]`.

**Theorem U1 [proved, given Theorem 11.56 (K1), whose statement and proof I read line by line; the two claims below
are checked by simulation, §1.4].**  Let `I_l` be an `r_l`-round procedure, and let `K` be computed with `L + 3` in
place of `L + 2` in its logarithm.  Then B2L⁺ is an algorithm with `r_1 + … + r_L` rounds which, for every `ψ ∈ L_u`,
(i) makes at most

    C_B = 1 + M_max(1 + C_1) + Σ_{l=2}^{L} N_l·C_l ,     N_l = K + (J+1)·max{ K , 4(1+η)c_η^{-1} e^λ · ν · e^{x_{l−1}} }

evaluations in every run, and (ii) with probability at least `1 − δ` returns exactly the bracket that Algorithm 2L⁺
returns with the same random choices — in particular a valid bracket of the accuracy stated in Theorem 11.56.

*Good event.*  `𝒢′ = 𝒢 ∩ (V3′)`, where `𝒢 = (V1) ∩ (V2) ∩ (V3)` is the good event of K1 and
(V3′): for all `j ≤ J`, `M ∈ ℳ`: `X_{s_j}(M) < K` or `X_{s_j}(M) ≤ (1+η)M·p(s_j)` (`X_t(M) = #{i ≤ M : W(a_i) > t}`).
These are `(J+1)(m_max+1)` further Chernoff events at fixed thresholds, each of probability at most `e^{-η²K/(3(1+η))}`
exactly as (V3); with `L+3` in place of `L+2` in `K` the total is still at most `δ`.

*Claim A (on `𝒢′`): every call `(i, l)` made by Algorithm 2L⁺ has `i ∈ C_l`.*  Induction on `l`; `l = 1` is trivial
(K1(iv): all sample sizes are at most `M̄ ≤ M_max`).  Let 2L⁺ call `I_l` for `a_i` during level `j` at a pass of size
`M ≥ i`.  The point is then at rung `l−1` and unclassified: `U_i > s_j` and `L_i ≤ s_je^{-b}`, where `[L_i, U_i]` is the
intersection of the results of rungs `0..l−1` — the stored bracket, because by induction `i ∈ C_{l'}` for `l' < l`.  By
K1(iv) (true for every run) `M ≤ max{K, 2M_j^neg} = max{K, 2ν s_j/(ℓ_je^b)}`, `ℓ_j` the value of `ℓ` at the entry of
level `j`.  It remains to show `ℓ_j ≥ λ_j`.  `ℓ_j ≥ ℓ₀`.  Let `i' < j`, `M' ∈ ℳ` with `N_L(i', M') ≥ K`.  The points
counted have `W ≥ L_i > s_{i'}` by (V1), so `X_{s_{i'}}(M') ≥ N_L(i', M') ≥ K` and (V3′) gives
`p(s_{i'}) ≥ N_L(i', M')/((1+η)M')`.  Level `i'` was left before level `j` was entered; by Step 7 of the proof of K1,
`s_{i'}q_{i'} ≤ e^bℓ_j/c_η` (populated: `q_{i'} ≤ p̲_{i'}/c_η` and `ℓ ≥ s_{i'}e^{-b}p̲_{i'}`; negligible:
`s_{i'}q_{i'} ≤ e^bℓ/((1−η)ν₀) ≤ e^bℓ`), and `q_{i'} ≥ p(s_{i'})` by Step 2.  Hence
`ℓ_j ≥ c_ηe^{-b}s_{i'}p(s_{i'}) ≥ c_η(1+η)^{-1}e^{-b}s_{i'}N_L(i', M')/M'`.  ∎

*Claim B (deterministic): `|C_l| ≤ N_l`,* provided every stored bracket of rung `l−1` has ratio at most `e^{x_{l−1}}`
(otherwise B2L⁺ has stopped) — the stored lower ends are at least `s₀` in any case, because the trivial bracket has
lower end `e^{-ψ(a,0)−un_i} ≥ s₀`.  At most `K` members have `i ≤ K`.  Fix `j` and let `i > K` be a member with witness
`j`; then `i ≤ 2ν s_j/(λ_je^b)` and `L_i ≥ U_ie^{-x_{l−1}} > s_je^{-x_{l−1}}`.  If `s_je^{-x_{l−1}} < s₀`, then
`i ≤ 2ν s_j/(ℓ₀e^b) ≤ 2ν(2p_u)^n e^{-b}·s_j/s₀ < 2ν e^{x_{l−1}}` (`s₀ ≤ (2p_u)^nℓ₀`).  Otherwise let `i'` be the largest
index with `s_{i'} ≤ s_je^{-x_{l−1}}`; `i' < j` and `s_{i'} > s_je^{-x_{l−1}−λ}`, and every such `i` is counted in
`N_L(i', M*)`, `M*` the smallest element of `ℳ` that is at least `min{M_max, 2ν s_j/(λ_je^b)}`, so
`M* ≤ max{K, 4ν s_j/(λ_je^b)}`.  If `N_L(i', M*) < K` there are fewer than `K` of them.  Otherwise the definition of
`λ_j` gives `N_L(i', M*) ≤ (1+η)c_η^{-1}e^bλ_jM*/s_{i'}`, and `M* = K` is impossible here (it would force
`i ≤ 2ν s_j/(λ_je^b) < K/2`), so `N_L(i', M*) ≤ 4(1+η)c_η^{-1}ν s_j/s_{i'} < 4(1+η)c_η^{-1}e^λν e^{x_{l−1}}`.  Summing
over the `J+1` levels gives `N_l`.  ∎  (The definition of `λ_j` as a maximum of *empirical* quantities is what makes
the count deterministic; no tolerance is lost because a coarse bracket that is high cannot have a low lower end.)

*Proof of the theorem.*  Rounds: stage `l` consists of the `r_l` batches of `I_l`, run in parallel on the fibres of
`C_l`; the sets `C_l` are computed between stages; the reference and trivial queries are part of the first batch.
Cost: Claim B, the stopping rule, and `M_max` calls of `I_1`.  On `𝒢′`, by Claim A, the output computation never asks
for a missing bracket, so it *is* a run of Algorithm 2L⁺ on the same randomness, and Theorem 11.56 applies.  Off `𝒢′`
the trivial bracket or a bracket of 2L⁺ is returned and the cost bound holds.  ∎

*Cost in exponents.*  `C_B` differs from `C_max` of Theorem 11.56 in two places: rung 1 is applied to all `M_max < 2M̄`
points (in K1: to `min{2M̄, (J+1)cnt(x₀)}`, the same number in every regime used so far), and `N_l ≤ 3·(J+1)cnt(x_{l−1})`.
So **every exponent statement derived from Theorem 11.56 — Corollary K1.b, Proposition 11.57(b), Theorems 11.54 and
11.58 — holds for the batched algorithm, with `Σ_l r_l` rounds.**

### 1.3 Consequences: the recursion in `r`

**Corollary U1.1 (round-limited ladders) [proved, given Theorem U1, Corollary K1.b, Theorem K2 and the assembly of
Proposition E of `K_REPORT.md`].**  Let `T^{(1)} = θ_na` on `(0, ∞)`, `T^{(1)}(0) = a` (the two-sample bracket of
Proposition 11.57(a) is one batch), and for `r ≥ 2`

    T^{(r)}(g) = min{ T^{(r−1)}(g) ,  inf  max{ μ + (1−φ)T^{(r_1)}(ξ_1) ,  max_{2≤l≤L} [ min(μ, (1−φ)ξ_{l−1}) + (1−φ)T^{(r_l)}(ξ_l) ] } },

the infimum over `0 < φ < 1`, `L ≥ 1`, `r_1 + … + r_L ≤ r` with `r_l ≤ r − 1`, rates `ξ_1 > … > ξ_L`, where for `g > 0`:
`ξ_L = β/(1−φ)`, `0 < β < g`, `μ = φθ_na((g−β)/φ)`, and for `g = 0` (bounded accuracy): `ξ_L = 0`, `μ = φa`.  Then for
every `r`, `g ≥ 0`, `g′ > g` and `ζ > 0` there is a family of `r`-round bracket procedures, valid on all of `L_u`, whose
exponent at the accuracy rate `g′` (at every bounded accuracy if `g = 0`) is at most `T^{(r)}(g) + ζ`.  Hence

    τ^{(r)} ≤ T^{(r)}(0),        and at accuracy ε₁n:   τ^{(r)}(ε₁) ≤ T^{(r)}(g)  for every g < ε₁.

*Proof.*  Induction on `r` exactly as in Proposition E(a) and Proposition K5(a) of `K_REPORT.md` (finitely many inner
families per step, each asked for an accuracy slightly above its nominal one), with Theorem U1 for the number of
rounds: rung `l` uses a family with `r_l` rounds, the ladder `Σ_l r_l ≤ r`.  ∎

**Corollary U1.2 (two rounds) [proved, as U1.1].**

    τ^{(2)} ≤ T^{(2)}(0) = min_{0<φ<1, ξ>0} max{ φa + (1−φ)θ_na(ξ) ,  min(φa, (1−φ)ξ) + (1−φ)a }  <  a.

The algorithm: `e^{φan}` uniform outer points; **round 1**: a two-sample bracket of accuracy `ξn_i` in every fibre
(`e^{(1−φ)nθ_na(ξ)}` points each) — this already gives every fibre average up to `e^{ξn_i}` and `A` up to about the same
factor; **round 2**: a two-sample bracket of bounded accuracy (`e^{(1−φ)na}` points) in the fibres of `C_2`, at most
`poly(n)·e^{ξn_i}` of them; then the layer-cake logic of 2L⁺ on the stored brackets.  Good event, validity, width:
those of Theorem 11.56.  For fixed `ξ` the two terms balance at `1−φ = a/(2a + ξ − θ_na(ξ))`, value
`a(a+ξ)/(2a + ξ − θ_na(ξ))`; at `ξ = h` this is `(a+h)/2` (because `θ_na(h) = h`), and the minimum is slightly lower.
In the small-slope limit `θ_na(x) = a(1 − √(x/a))²` the value is `a(1+ξ′)/(1+2√ξ′)` with `ξ′ = ξ/a`, minimal at
`√ξ′ = (√5−1)/2`: `T^{(2)}(0) = ((√5−1)/2)·a = 0.618a` **[proved]**.  Numbers (`ub2_closed.py`, direct minimisation):

| `u` | `→ 0` | `0.5` | `1` | `2` | `3` |
|---|---|---|---|---|---|
| `T^{(2)}(0)/a` | 0.6180 | 0.6196 | 0.6243 | 0.6412 | 0.6646 |
| `(a+h)/(2a)` | 0.625 | 0.6266 | 0.6313 | 0.6484 | 0.6720 |

**The recursion evaluated [numerical; `ub_rounds.py`, conservative grids — every number is an upper bound for the
recursion].**  `T^{(r)}(0)/a`:

| `r` | 2 | 3 | 4 | 5 | 6 | 8 | 12 | 16 | 24 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| small-slope limit (`h/a = 0.25`) | 0.619 | 0.535 | 0.471 | 0.444 | 0.430 | 0.408 | 0.382 | 0.368 | 0.351 | 0.341 | – | – |
| `u = 1` (`h/a = 0.2626`) | 0.625 | 0.541 | 0.481 | 0.454 | 0.440 | 0.421 | 0.394 | 0.379 | 0.364 | 0.354 | 0.342 | 0.335 |

(The second row for `r ≥ 24` is from a run in which ladders may only use inner procedures with
`1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48` rounds; with all round numbers allowed `r = 24, 32` give `0.3632, 0.3530`.)
Necessary conditions, all satisfied: one-round product samples do not beat `θ_na` (the minimum of
`φθ_na((g−β)/φ) + (1−φ)θ_na(β/(1−φ)) − θ_na(g)` over a grid is `−2·10^{-16}`); `T^{(r)} ≥ θ_hint` on the whole grid for
every `r`; `T^{(r)}` is nonincreasing in `r`; `T^{(2)}(0) ≥ θ₂*` of Theorem U3.  Reading: three rounds are two levels
with three rungs or three levels `(2,1)`; four rounds already beat the two-level value with an infinitely fine
ladder (`0.481a < τ₂ = 0.5006a`); `(T^{(r)}(0) − h)/a = 0.363, 0.278, 0.219, 0.158, 0.117, 0.091, 0.073` for
`r = 2, 3, 4, 8, 16, 32, 64` — about `0.36/(log₂ r)^p` with `p` rising from `0.75` to `0.9` **[numerical]**.

**Corollary U1.3 (`τ^{(r)} → h`) [proved, given Theorem U1 and the proof of Theorem 11.58].**  For every `η > 0` there
is `r(η) < ∞`, independent of `n`, with `τ^{(r(η))} ≤ h + 3η`.  Indeed the algorithm in the proof of Theorem 11.58 for a
given `η` consists of `m ≈ ln(a/h)·a/η` two-rung levels on top of one extensive family, which itself has a fixed number
`k` of levels with fixed finite ladders; none of these numbers depends on `n`.  By Theorem U1 the family `G_m` of that
proof needs `R(G_m) ≤ R_E + R(G_{m−1})` rounds (rung 1: the extensive family, `R_E` rounds; rung 2: `G_{m−1}`), i.e. at
most `(m+1)·R_E` rounds, with `R_E ≤ L^{k−1}` for ladders of at most `L` rungs.  *Rate:* the proof gives no usable bound on `k(η)`;
with the numerical law `τ_k − h ≈ 0.65a/k²` of §11.19 and ladders of `L ≈ u/η` rungs one gets
`r(η) = exp(O(η^{-1/2} ln(1/η)))`, i.e. `τ^{(r)} − h = O((ln ln r/ln r)²)` **[numerical/heuristic, not proved]**.

**Relation to the level values.**  `k` levels whose ladders have `L_1, …, L_{k−1}` rungs (outermost first) over
one-round brackets are `L_1⋯L_{k−1}` rounds, so `τ^{(L^{k−1})} ≤ τ_k^{[L]}`, the `k`-level exponent with `L`-rung ladders,
and `τ_k^{[L]} ↓ τ_k` as `L → ∞`; `lim_r τ^{(r)} ≤ τ_k` for every `k` is all that the level values say about rounds.

### 1.4 Harness for Theorem U1 — `batched_ladder_sim.py`

Own implementation of the outer loop of 2L⁺ from the text of `K_REPORT.md` §2.2, of the sets `C_l`, and of a
simulated inner oracle (bracket `[We^{-αx_l}, We^{(1−α)x_l}]`, `α` uniform / all 0 / all 1 / mixed, attached to the
pair `(i, l)`), on product instances `ψ(a,b) = F_o(d(a,s_o)) + c_i·d(b,s_i)` with `n_o ≤ 10`, six kinds of outer
profiles (flat, cone, dip, truncated cone, random walk, flat histogram), ladders of 2–4 rungs, the constants of the
theorem except `K ∈ {6, 10, 16}` and `η′ ∈ {1, 20, 100}` (so that the selection is not vacuous: about 11 % of the
sampled points are candidates for rung 2), samples of up to `4·10⁶` outer points.  `u = 1`: 150 runs, all closed; in
the 125 runs in which the certificates of the levels left and (V3′) hold, **every call of the sequential algorithm is
in `C_l`** (Claim A); **`|C_l| ≤ N_l` in all 150 runs** (largest ratio 0.016 — the bound is far from tight at these
sizes); 135 levels were left as negligible; in the 25 runs where the events fail no containment failure occurred
either.  Two mutations are detected: `λ_j` without the factor `c_ηe^{-b}/(1+η)` — 10 runs violate Claim A; `M̂_j`
without the factor 2 — 4 runs.  The same at `u = 3` with another seed: 100 runs, 82 with the events, no violation of
either claim, 348 negligible levels, the mutations detected in 13 and 7 runs.  A first version of the harness reported two violations of Claim A that were a bug
of my sequential implementation (a point was advanced two rungs in one pass without re-testing; found by printing
the offending brackets).  *Not exercised:* real inner brackets; nested levels; sizes at which `C_l` is a small
fraction of the sample.

---

## 2. A lower bound for two rounds above the hinted exponent

### 2.1 Block-radial functions and Lemma U2

Split the coordinates into blocks, `Q_n = Q_{n_1} × … × Q_{n_m}`, `n_j = φ_jn`, and let `s = (s¹, …, s^m)` be centres.
A *block-radial* function is `ψ_s(x) = F(d(x¹,s¹), …, d(x^m,s^m))` with `F` defined on the grid of *types*
`d = (d_1, …, d_m)`, `0 ≤ d_j ≤ n_j`.  `ψ_s ∈ L_u(Q_n)` iff `F` changes by at most `u` when one `d_j` changes by one
(one flip changes one block distance by one), and `A(ψ_s) = Σ_d Π_j P_j(d_j)·e^{-F(d)}` with `P_j = Bin(n_j, ½)` does not
depend on `s`.  `BR_m = BR_m(φ_1, …, φ_m)` denotes this class; `R_u ⊂ BR_2 ⊂ L_u` (a radial function is
`F(d_1,d_2) = f(d_1+d_2)`).

**Lemma U2 (what `r` batches can see) [proved].**  Let `F, F′` be two such functions on `m = r` blocks and
`𝒲_1, …, 𝒲_r` sets of types such that
(a) `F = F′` on every `𝒲_t`;
(b) for `t < r`: on `𝒲_t`, `F` depends only on `(d_1, …, d_t)`.
Let `p_t = max_{d_1..d_{t−1}} P( (d_1, …, d_{t−1}, D_t, …, D_r) ∉ 𝒲_t )` for independent `D_j ∼ Bin(n_j, ½)`.  Then for every
randomised `r`-round algorithm with batch sizes at most `M_1, …, M_r`, and centres drawn uniformly at random, the
transcripts (queries and answers) on `ψ_s` and on `ψ′_s` can be coupled so that they differ with probability at
most `Σ_t M_tp_t`.  Consequently, if the algorithm is `(ε/2, δ)`-correct on `L_u` and `|ln A(F) − ln A(F′)| > ε`, then

    Σ_t M_t p_t ≥ 1 − 2δ.

*Proof.*  Fix the coins of the algorithm and use the same centres for both instances.  Let `E_t` be the event that
all points of batch `t` have types in `𝒲_t`.  On `E_1 ∩ … ∩ E_{t−1}` the answers to the first `t−1` batches are the same
for `F` and `F′` by (a), and by (b) they are functions of the coins and of `s¹, …, s^{t−1}` only; hence so is batch `t`
(for both instances).  Conditionally on `s¹, …, s^{t−1}` the centres `s^t, …, s^r` are uniform and independent of that
batch, so for each of its points the distances `(d_t, …, d_r)` are independent binomials, whatever the point is and
whatever its distances to the known centres are: `P(E_t^c | E_{<t}, s^{<t}) ≤ M_tp_t`.  On `∩_tE_t` the two transcripts
coincide.  If both outputs were within `ε/2` of the respective `ln A` they would differ; correctness on each instance
(for every `s`, hence on average) gives `P(outputs differ) ≥ 1 − 2δ`.  ∎

Remarks.  (1) The algorithm is *given more than it can know*: nothing is assumed about what it learns of
`s¹, …, s^{t}` from batch `t`.  (2) `r = 1`, one block: `𝒲_1 = {f(d/n) ≤ θ}`, `F′` = the flat histogram `g` defined below, `F` = the lower McShane
envelope of `g` from `𝒲_1` (below the shells that the batch sees it continues as a cone); the gap is
`n·k(f^{-1}(θ)) − O(log n) > 0` for `θ < a`: Lemma U2 reproduces the non-adaptive bound `a` of Theorem 11.45 with a
different pair.  (3) One block, `F = 0`, `F′` a critical dip, every `𝒲_t` the set of types of rate at most `θ < h`
(nothing is ever revealed): the hinted bound `h`, for any number of rounds.  So the lemma passes the two necessary
conditions `τ^{(1)} = a`, `τ^{(∞)} ≥ h`.

### 2.2 Theorem U3

For `0 < φ₁ < 1`, `φ₂ = 1 − φ₁`, `0 < θ < φ₂ ln 2` put

    E_θ(c) = φ₁·x_na(c/φ₁) + φ₂·D((θ − c)/φ₂),     0 ≤ c ≤ min(θ, φ₁a),          Ξ(θ, φ₁) = min_c E_θ(c).

In terms of radii: `c = φ₁f(z)`, `p_u ≤ z ≤ ½`; `ρ^s(z)` is the block-2 radius with `φ₂f(ρ^s) = θ − φ₁f(z)`; and
`E = φ₁k(z) + φ₂(uρ^s(z) − Λ₁)`.

**Theorem U3 (two rounds do not reach the hinted exponent) [proved; the finite-`n` version by exact computation,
`lb2_exact.py`].**  Let `u > 0`, and let `φ₁, θ` satisfy

    Ξ(θ, φ₁) > 0      and      θ < φ₂a.

Let `y¹ ∈ (p_u, ½)` be the radius with `φ₂f(y¹) = θ` and `γ = min{Ξ(θ,φ₁), φ₂k(y¹)} > 0`.  Then for every `ε₁ < γ`,
`δ < ½` and all `n ≥ n₀(u, φ₁, θ, ε₁)`: every two-round algorithm that is `(ε/2, δ)`-correct on `L_u(Q_n)` for some
accuracy `ε ≤ ε₁n` uses batches with

    max(M₁, M₂) ≥ (1 − 2δ)·e^{nθ} / (2(n+1)²).

Hence `τ^{(2)} ≥ θ₂*(u) := sup{θ : Ξ(θ,φ₁) > 0 and θ < φ₂a for some φ₁}`, also at extensive accuracies below `γn`, and

    θ₂*(u) > h      for every u > 0.

*The pair.*  `n₁ = ⌊φ₁n⌋`, `n₂ = n − n₁`, `T = nθ`, `c_j(d) = −ln P_j(d)`.
* `W₁ = {(d₁,d₂) : c₁(d₁) + c₂(d₂) ≤ T}`, `W₂ = {d₂ : c₂(d₂) ≤ T}` (a central interval `[lo₂, n₂ − lo₂]`),
  `V₂ = {(d₁,d₂) : d₂ ∈ W₂} ⊃ W₁`.  Then `p₁ := P((D₁,D₂) ∉ W₁) ≤ (n+1)²e^{-nθ}` and `p₂ := P(D₂ ∉ W₂) ≤ (n+1)e^{-nθ}`
  (every type outside has probability below `e^{-T}`).
* *Flat histogram:* `t_j(d) = ln P_j(mode) − ln P_j(d) ≥ 0`, and `g_j = −`(the largest `u`-Lipschitz minorant of `t_j`).
  `g_j = −t_j` wherever `t_j` has slope at most `u`, i.e. for `p_u + O(1/n) ≤ d/n_j ≤ 1 − p_u − O(1/n)`; there
  `P_j(d)e^{-g_j(d)} = P_j(mode)`: all these shells carry the same mass.  Always `P_j(d)e^{-g_j(d)} ≤ P_j(mode) ≤ 1`.
* `F_deep(d) = max_{e ∈ W₁} [ g₁(e₁) − u|d₁−e₁| − u|d₂−e₂| ]` (the lower McShane envelope of `g₁` from `W₁`: the deepest
  `u`-Lipschitz function that equals `g₁(d₁)` on `W₁`);
  `F_cap = max(F_deep, g₁(d₁) + g₂(d₂))` (`= g₁` on `W₁`, since `g₂ ≤ 0`);
  `F_D(d₁,d₂) = F_cap(d₁, b) − u|d₂ − b|` and `F_S(d₁,d₂) = F_cap(d₁, b) + u|d₂ − b|` for `d₂ ∉ W₂`, `b` the nearer end
  point of `W₂`; `F_D = F_S = F_cap` on `V₂`.
All four are `u`-Lipschitz in each argument (maxima of such functions; extension along `d₂` at slope `±u`).  The
twins `(F_D, F_S)` satisfy the hypotheses of Lemma U2 with `𝒲_1 = W₁`, `𝒲_2 = V₂`: they coincide on `V₂ ⊃ W₁`, and
on `W₁` they equal `g₁(d₁)`.

*Proof.*  By Lemma U2, `M₁p₁ + M₂p₂ ≥ 1 − 2δ` as soon as `ln A(F_D) − ln A(F_S) > ε`; it remains to bound the gap.
(1) `A(F_S) ≤ (n₁+1)(n₂+1)`.  On `V₂`, `F_S = F_cap ≥ g₁ + g₂`, so every type has mass
`P₁P₂e^{-F_S} ≤ P₁e^{-g₁}·P₂e^{-g₂} ≤ 1`; for `d₂ < lo₂` the mass is that of `(d₁, lo₂)` times
`P₂(d₂)e^{-u(lo₂−d₂)}/P₂(lo₂) ≤ 1`, and symmetrically above.
(2) `A(F_D) ≥` the mass of the single type `(x₀, y₀) = (⌈p_un₁⌉+1, ⌈p_un₂⌉+1)`; `y₀ < lo₂` for large `n` because
`lo₂/n₂ → y¹ > p_u` (this is where `θ < φ₂a` is used).  Its logarithm is

    [ln P₁(x₀) + ln P₂(lo₂) − F_cap(x₀, lo₂)] + [ln P₂(y₀) − ln P₂(lo₂) + u(lo₂ − y₀)].

The second bracket is `n₂(k(lo₂/n₂) − k(y₀/n₂)) + O(log n) = nφ₂k(y¹) − o(n)` (as `c₂(d) + ud = n₂(Λ₁ + k(d/n₂)) + O(log n)`).
In the first, `−F_cap = min(−F_deep, −g₁ − g₂)`; with `−g₁(x₀) − g₂(lo₂) = t₁(x₀) + t₂(lo₂)` (both in the flat range)
the second alternative gives `ln P₁(mode) + ln P₂(mode) ≥ −2 ln(n+1)`.  For the first alternative,

    −F_deep(x₀, lo₂) = min_{e₁} [ −g₁(e₁) + u|x₀ − e₁| + u(lo(e₁) − lo₂) ],

`[lo(e₁), n₂ − lo(e₁)]` being the slice of `W₁` at `e₁` (`lo(e₁) ≥ lo₂`).  Shells `e₁` outside the flat range are
dominated by the end point `e*` of that range on the same side (`−g₁(e₁) = t₁(e*) + u|e₁−e*|`, the triangle
inequality, and `lo(e₁) ≥ lo(e*)`), and shells beyond `n₁/2` by their mirror images.  For `e₁ = zn₁`, `p_u ≤ z ≤ ½`:
`−g₁(e₁) = t₁(e₁) ≥ n₁f(z) − ln(n+1)`; `c₂(lo(e₁)) ≤ T − c₁(e₁)` gives `lo(e₁)/n₂ ≥ f^{-1}((nθ − n₁f(z))/n₂)`, which
converges to `ρ^s(z)` uniformly in `z`; and `lo₂/n₂ → y¹`.  Therefore

    n^{-1}[ln P₁(x₀) + ln P₂(lo₂) − F_deep(x₀, lo₂)] ≥ min_{z ≥ p_u, φ₁f(z) ≤ θ} [φ₁f(z) + uφ₁(z − p_u) + uφ₂(ρ^s(z) − y¹)] − φ₁a − θ − o(1)
                                                   = min_z [φ₁k(z) + φ₂(uρ^s(z) − Λ₁)] − φ₂k(y¹) − o(1) = Ξ − φ₂k(y¹) − o(1)

(using `f(z) + uz = Λ₁ + k(z)`, `a + up_u = Λ₁`, `θ = φ₂f(y¹)`).  Together:
`ln A(F_D) ≥ n·min{Ξ − φ₂k(y¹), 0} + nφ₂k(y¹) − o(n) = nγ − o(n)`.
(3) So `ln A(F_D) − ln A(F_S) ≥ nγ − o(n) > ε₁n ≥ ε` for large `n`, and `max(M₁,M₂)(p₁+p₂) ≥ 1 − 2δ` with
`p₁ + p₂ ≤ 2(n+1)²e^{-nθ}`.
(4) `θ₂* > h`.  `f` is convex and decreasing on `[0, ½]`, so `f(φ₁z + φ₂ρ^s) ≤ φ₁f(z) + φ₂f(ρ^s) = θ` gives
`φ₁z + φ₂ρ^s ≥ f^{-1}(θ)` and

    E_θ(c) = c + u(φ₁z + φ₂ρ^s) − Λ₁ ≥ c + D(θ).

At `θ = h`: `E_h(c) ≥ c`, and `E_h(0) > 0` because at `c = 0` Jensen's inequality is strict (`z = ½ ≠ ρ^s`); `E_h` is
continuous on a compact interval, so `Ξ(h, φ₁) > 0` for every `φ₁ ∈ (0,1)`.  `Ξ` is continuous in `θ`, and
`h < φ₂a` for `φ₁ < 1 − h/a`; so both conditions hold for some `θ > h`.  ∎

*Numbers [numerical; `lb2_exponent.py`, `ub2_closed.py`].*  `θ₂*(φ₁) = min{φ₂a, root of Ξ(·,φ₁)}`; the root increases
and `φ₂a` decreases with `φ₁`, and the best `φ₁` is where they meet.

| `u` | `→ 0` | `0.25` | `0.5` | `1` | `2` | `3` | `4` | `6` |
|---|---|---|---|---|---|---|---|---|
| best `φ₁` | 0.654 | 0.653 | 0.651 | 0.641 | 0.606 | 0.560 | 0.512 | 0.425 |
| `θ₂*/a` | 0.346 | 0.347 | 0.350 | 0.359 | 0.394 | 0.440 | 0.488 | 0.575 |
| `θ₂*/h` | 1.384 | 1.383 | 1.380 | 1.368 | 1.328 | 1.277 | 1.229 | 1.156 |
| `h/a` | 0.250 | 0.251 | 0.253 | 0.263 | 0.297 | 0.344 | 0.397 | 0.497 |
| `T^{(2)}(0)/a` (upper bound) | 0.618 | – | 0.620 | 0.624 | 0.641 | 0.665 | – | – |

In the small-slope limit (units `a = 1`): `Ξ = 1 + min_c [c − 2√(φ₁c) − 2√(φ₂(θ−c))]`, and `Ξ(h, φ₁) = +0.017, 0.054,
0.096, 0.132` at `φ₁ = 0.1, 0.3, 0.5, 0.65`.  **So at every `u` the two-round exponent lies in `[θ₂*, T^{(2)}(0)]`,
e.g. `[0.359a, 0.624a]` at `u = 1`, strictly between `h = 0.263a` and `a`.**

*Exact finite-`n` evaluation [numerical: exact binomial arithmetic in log space; `lb2_exact.py`].*  For each `n` the
largest `T` (over `n₁/n ∈ {0.45, …, 0.68}`) for which the twins have `ln A(F_D) − ln A(F_S) > 1`; here `W₂` is the
smallest central interval with `p₂ ≤ p₁` (so `W₁ ⊄ V₂` in general, the first batch must stay in `W₁ ∩ V₂`, and the
bound reads `max(M₁,M₂) ≥ (1−2δ)/(p₁ + 2p₂)`).  `E = −n^{-1}ln(p₁ + 2p₂)`; last column: the exponent
`n^{-1}ln(2ⁿ/|B(n,k*(1))|)` of the hinted lower bound of Theorem 11.25(a) at the same accuracy.

| `u = 1` (`h = 0.02914`), `n` | `n₁` | gap | `E` | `E/h` | hinted bound |
|---|---|---|---|---|---|
| 400 | 200 | 1.05 | 0.03190 | 1.095 | 0.03477 |
| 800 | 400 | 1.07 | 0.03387 | 1.162 | 0.03234 |
| 1 600 | 880 | 1.04 | 0.03598 | 1.235 | 0.03092 |
| 3 200 | 1 760 | 1.01 | 0.03661 | 1.256 | 0.03011 |
| 6 400 | 3 584 | 1.00 | 0.03720 | 1.277 | 0.02973 |
| 12 800 | 7 680 | 1.00 | 0.03824 | 1.312 | 0.02943 |

| `u = 2` (`h = 0.09728`), `n` | `n₁` | gap | `E` | `E/h` | hinted bound |
|---|---|---|---|---|---|
| 200 | 90 | 1.05 | 0.11165 | 1.148 | 0.11164 |
| 400 | 200 | 1.16 | 0.11570 | 1.189 | 0.10441 |
| 1 600 | 880 | 1.05 | 0.12244 | 1.259 | 0.09934 |
| 6 400 | 3 584 | 1.23 | 0.12461 | 1.281 | 0.09789 |

On every pair the script checks: both functions are `u`-Lipschitz in each argument; `F_D = F_S = g₁` on `W₁ ∩ V₂`;
`F_D = F_S` on `V₂`; `F_S ≥ F_D`.  At `u = 1` the two-round bound overtakes the hinted bound between `n = 400` and
`n = 800`; at `n = 12 800` it is `e^{0.0382n} = e^{489}` against `e^{377}`.  The limit `θ₂*/h = 1.368` is approached
slowly (the gap must exceed a constant, which costs `O(log n/n)` in `θ`).
*The asymptotic formula against exact values* (`diag_lb2.py`, `φ₁ = 0.6`, `n = 12 800`): at effective exponents
`θ = 0.0293, 0.0333, 0.0373, 0.0413` the exact `n^{-1}[ln A(F_D) − ln A(F_S)]` is `0.00158, 0.00071, 0.00016, 0.00000`,
the prediction `min(Ξ, φ₂k(y¹))₊` is `0.00175, 0.00089, 0.00035, 0` (the differences shrink from `n = 1600` to
`12 800` like `log n/n`); the bulk type of `F_D` is `(p_u, p_u)` up to the symmetry `d ↔ n_j − d`, as in the proof.
*Whole cubes* (`small_cube_checks.py`): for `(n₁,n₂) = (6,6), (8,6), (8,8), (9,7), (7,9)` and random centres, `ψ = F_D`
and `ψ = F_S` as functions on all `2ⁿ` points have largest edge difference exactly `u`, `ln A` by enumeration agrees
with the sum over types to 10 digits, and the twins coincide on the points whose type is in `V₂`.  Lemma U2 by
simulation (types only, round 2 choosing `d₁` freely): the frequency with which some answer differs is below
`M₁(p₁+p₂) + M₂p₂` in all five parameter sets.

### 2.3 What the instance is, and why two rounds fail on it

`F_cap` restricted to what the batches see is: a radial function of the first block that makes every shell
`p_u ≤ d₁/n₁ ≤ ½` equally heavy (`e^{-g₁}` is the reciprocal of the binomial weight), and, on each shell, a dip in the
second block that starts exactly where a blind sample of `e^{nθ}` points stops seeing that shell: a point of shell
`z` has probability `e^{-nφ₁f(z)}`, so the sample has `e^{n(θ − φ₁f(z))}` points there and sees the second block only down
to the radius `ρ^s(z)`.  The Lipschitz condition couples the shells — the dip cannot be much deeper on one shell than
on its neighbours — and `min_c E_θ(c)` is the result of that coupling: the binding shell is the one with
`1/s(z) = 1 + 1/s(ρ^s(z))`, `s(ρ) = |f′(ρ)|/u`, where the unused slope `u(1 − s(z))` of the flat histogram is exactly
what the growth of the dip from shell to shell consumes.  After round 1 the algorithm knows `s¹` and nothing about
`s²`.  In round 2 it can place `e^{nθ}` points on *every* shell and sees the second block down to `y¹` there: the rim
of the dip, and with it `s²` — but the mass of the dip sits at radius `p_u < y¹` of the second block, where the twin
`F_S` has no dip.  A third round reads it off: the three-round algorithm for block-radial functions of §5.2 costs
`e^{nh+o(n)}` on this instance (round 1 at budget `h` reveals `s¹`, round 2 the rim on the shells of cost at least
`θ − h`, round 3 everything).

Two features are essential and both are absent from "nested basins with hidden centres": the first-round structure
is *not* localised (it has no plateau; every shell matters equally, which is what dilutes the first batch), and the
second structure is *additive* in a fresh block, not shielded by the first (shielding costs mass, §3.3).

### 2.4 Three rounds: the same idea gives nothing **[numerical, small-slope limit]**

The natural continuation has three blocks: a flat histogram in block 1 seen by round 1, a structure in block 2
that round 1 cannot see and round 2 can, a dip in block 3 that only round 3 could follow.  The deepest functions
compatible with what the batches see are again capped lower McShane envelopes, and their hidden gain is
(`lbr_gauss.py`; units `a = 1`, `h = ¼`; block `j` has the coordinate `Y_j ∈ [0, σ_j]`, `σ_j² = φ_j`, rate `Y_j²`, metric
`2Σσ_j|ΔY_j|`)

    m₂(X₁; Z₂) = min{ 0 ,  min_{Z₁} [ Z₁² − X₁² + 2σ₁|X₁ − Z₁| + 2σ₂(Z₂ − √(θ − Z₁²))₊ ] − Z₂² },
    Ξ₃(θ)      = max_{X₁} min_{Z₂} [ m₂(X₁; Z₂) + (σ₂ − Z₂)² + σ₃² − 2σ₃√(θ − Z₂²) ],

three rounds failing if `Ξ₃ > 0` and `θ < φ₃`.  Result: **`Ξ₃(h) < 0` for every split tried**
(`φ₁ ∈ {0.0005, …, 0.3}`, `φ₃ ∈ {0.26, …, 0.9}`; e.g. `−0.00025, −0.0050, −0.0487, −0.094` at
`φ₁ = 0.0005, 0.01, 0.1, 0.2`), the largest `θ` with `Ξ₃ > 0` on the grid is `0.2495 < h`, and for small `φ₁`
`Ξ₃(h) = d − √d ≈ −φ₁/2` with `d = 1 − φ₁`, independently of how `d` is split.  The reason is visible in the formula:
round 2 knows `s¹` and has the full budget `θ` on the remaining cube of dimension `dn` — more than that cube's own
hinted exponent `dh` — and wherever the block-2 structure is not yet open (`m₂ = −Z₂²`), blocks 2 and 3 together
form a plain dip of the smaller cube, which is subcritical: `d − 2√(dθ) < 0`.  Opening the block-2 structure early
enough to avoid this requires hiding it from round 1 by dilution, which (heuristically) needs `φ₁ ≳ 2θ`, and then `d`
is too small.
The formulas are checked against an independent brute-force construction on grids (`lbr_gauss_bruteforce.py`: the
envelopes computed by separable sweeps on `400²` and `90³` points): `r = 2`: hidden gain `= min(Ξ₂, (σ₂−√θ)²)` to three
digits in six cases; `r = 3`: `−0.0483, −0.0733, −0.0896, −0.0242, −0.1103` against `−0.0487, −0.0748, −0.0922, −0.0247,
−0.1131` from the formula.  I did not do the three-block computation at finite `u`, and I have no proof that no
other three-round family works.  **Whether `τ^{(3)} > h` is open** (§8).

---

## 3. Q3 — what one round can do

### 3.1 The conditional covering exponent

**Proposition U6 [proved; exact counting in `cond_cover.py`].**  Let `x₁ ∈ Q_n` be known and let the target be a ball
`B(s, κn)`, `κ < ½`, whose centre `s` is uniform on the sphere of radius `σn` around `x₁`, `σ ≤ ½`.
(a) *Dual bound.*  Every point lies in the ball with probability at most `|B(n,κn)|/C(n,σn)`; a batch that hits the
ball with probability `1 − 2δ` has at least `(1−2δ)C(n,σn)/|B(n,κn)| = exp(n(f(κ) − f(σ)) − o(n))` points.
(b) *Primal bound.*  If `σ ≤ κ` the single point `x₁` hits.  If `σ > κ`, points uniform on the sphere of radius `t*n`
around `x₁`, `t* = (σ − κ)/(1 − 2κ)`, hit with probability `exp(−n(f(κ) − f(σ)) − o(n))`.
So the least cost is `exp(n·(f(κ) − f(σ))₊ + o(n))`: the *conditional covering exponent* `cov(σ, κ) = (f(κ) − f(σ))₊`.
If only "`s ∈ B(x₁, ρn)`" is known, the worst prior is the sphere of radius `ρn` and the exponent is `(f(κ) − f(ρ))₊`;
if in addition the ball must lie inside `B(x₁, ρn)` (next subsection), it is `(f(κ) − f(ρ − κ))₊`.
*Proof.*  (a) A point `x` hits iff `s ∈ B(x, κn)`, and `B(x,κn)` contains at most `|B(n,κn)|` of the `C(n,σn)` possible
centres.  (b) For `x` at distance `tn` from `x₁`, the number of centres within distance `κn` of `x` is
`Σ_{i ≥ (t+σ−κ)n/2} C(tn, i)·C((1−t)n, σn − i)` (`i` = number of coordinates in which both `x` and `s` differ from `x₁`).
With `t = t*` the typical point of the sphere of radius `κn` around `x` (which flips a fraction `κ` of the `tn` and of
the `(1−t)n` coordinates) is at distance `(t + κ − 2tκ)n = σn` from `x₁`, so the sum is `e^{nH(κ) − o(n)}` (`H` the
entropy), and `C(n,σn) = e^{nH(σ)+o(n)}`.  ∎
`cond_cover.py` evaluates the sum exactly for seven pairs `(σ,κ)` and `n = 200, 800, 3200`: the best `t` is `t*` to
three digits, and `min_t` cost`/n` lies between the counting bound and `H(σ) − H(κ) + O(log n/n)`
(e.g. `σ = 0.45, κ = 0.38`: `0.02500` at `n = 3200`, bounds `0.02377` and `0.02407`).
This is the basic step of every "descent" in which the next structure is a ball; note that the knowledge of `x₁`
is worth exactly the factor `e^{nf(σ)}`, the reciprocal measure of the sphere on which the centre is known to lie.

### 3.2 Balls hide only what they contain

**Proposition U7 (shadows) [proved].**  Let `ψ₁(x) = −D + u(d(x,s₁) − R)₊` (a plateau `B(s₁,R)` at level `−D`),
`ψ₂(x) = −D − uK + u·d(x,s₂)` (a cone that dips `uK` below the plateau), `ψ = min(ψ₁, ψ₂) ∈ L_u`.
(a) If `d(s₁,s₂) + K ≤ R`, then `{ψ₂ < ψ₁}` is the open ball `B°(s₂, K) ⊂ B(s₁, R)`: outside it `ψ = ψ₁`.
(b) If `d(s₁,s₂) + K ≥ R + 3`, then `ψ = ψ₂` at the antipode `s̄₁` of `s₁` and at its `n` neighbours, and these `n+1`
values determine `s₂` and `K`: an algorithm that knows `s₁` finds the dip with `n + 1` evaluations.
*Proof.*  (a) If `d(x,s₂) ≥ K`: `ψ₂(x) + D = u(d(x,s₂) − K) ≥ u(d(x,s₁) − R)` by the triangle inequality
`d(x,s₁) ≤ d(x,s₂) + R − K`, and `≥ 0`.  (b) `ψ₁(s̄₁) − ψ₂(s̄₁) = u(n − R) + uK − u(n − d(s₁,s₂)) ≥ 3u`; at a neighbour `ψ₁`
drops by `u` and `ψ₂` changes by `±u`, so `ψ = ψ₂` there too, and the sign of the change tells the coordinate of `s₂`.
∎
So a nest of balls can hide the next centre only if the next *ball* lies inside the plateau: with all radii at
least `p_un` (a structure that matters has that radius) hiding by nesting needs plateaus of radius above `2p_un`,
which for `u ≲ 1.1` is more than half the cube.  This is why nested balls in one cube do not even get started at
moderate slopes.

### 3.3 Nests of cones do not separate two rounds from many **[sketch + numerical; an idealised game]**

To test observation (iii) beyond balls I analysed max–min nests of cones with independent centres,
`ψ = max(c₁, min(L₁, max(c₂, min(L₂, …))))`, `c_j = b_j + u·d(·,s_j)` (the maximum with `c_j` removes the shadows of
Proposition U7; the region of level `m` is `∩_{j≤m} B(s_j, r_j(L_{m−1}))`), in the idealised game in which a hit of
the region of level `m` reveals `s₁..s_m` (for exact cones this costs `n^{O(m)}` local evaluations in the same
batch).  In the small-slope limit (units `a = 1`; level `j` opens at depth `λ_{j−1}` with threshold `τ_j`; at depth `λ`
the threshold of an open direction is `y_j(λ) = τ_j + λ − λ_{j−1}`): the cost of reaching level `m` knowing levels
`≤ i` is `J(i→m) = Σ_{i<j≤m} y_j(λ_{m−1})²` — additive, as in pointer chasing —, the mass at depth `λ` is
`2λ − Σ_j y_j(λ)²`, and the last level must carry the largest mass.
* *Numerics* (`explore_gauss_on2.py`: `1.2·10⁵` random instances per case and ten rounds of resampling, up to four
  levels, every pattern of "new direction / truncation of the previous cone"): the largest one-round value is
  `1.000` (`= a`: the necessary condition), and **the largest `r`-round value is `0.2500 = h` for every `r ≥ 2`**,
  attained by the single dip.  The same at `u = 1` with exact binomial rates (`explore_onu.py`): `a` and `h`.
* *Why* (the erosion inequality; a proof for the case that the blind cost passes `¼` inside a level, a sketch
  otherwise): let round 1 go blind to the depth `λ′` where `Σ_{j≤m₀} y_j(λ′)² = ¼`.  Going `x` deeper raises every open
  threshold by `x`, so the old directions cost `¼ + 2xS + m₀x²` with `S = Σy_j(λ′) ≥ ½`; the final level must weigh at
  least as much as depth `λ′`, which leaves `N ≤ 2x − 2xS − m₀x² ≤ x − x² ≤ ¼` for the squared thresholds of all new
  directions together.  So round 2, which knows the old centres, reaches the bottom at cost `≤ e^{nh}`: *deep
  implies wide, and what a blind batch of `e^{nh}` points has not reached is cheap from where it stands.*
* *A trap.*  At `u = 4` the same script returns a one-round value `1.087a > a`.  The necessary condition fails
  because the model does: for independent centres the measure of an intersection of balls is the product of the
  measures only on average over the centres; two balls of radius below `n/4` around centres at distance `n/2` are
  disjoint.  The model is sound only while the radii are large (small and moderate `u`).
The two-round family of §2 is not of this kind (§2.3).

### 3.4 The type game: a variational problem for block-radial classes

On `BR_m` with uniformly random centres the situation of §2.1 is exact in both directions.  A batch that knows the
centres of the blocks in `S` can give its points any distances to those centres, and for the other blocks its
points are typical: with `e^{nθ}` points it sees the types `V_S(θ) = {δ : Σ_{j∉S} φ_jf(δ_j) ≤ θ}` and no others (Lemma
U2 for "no others"; uniform sampling of the unknown blocks, shell by shell in the known ones, for "sees").  The
centre of block `j` becomes known when `F` depends on `δ_j` at a type that is seen (two different values among the
block-`j` neighbours of a sampled point, as in Theorem 11.51).  So an `r`-round algorithm generates a chain
`∅ = S₀ ⊂ S₁ ⊂ … `, `S_t` = the blocks on which `F` depends inside `V_{S_{t−1}}(θ)`, and after the last batch it knows `F`
on `V_{S_{r−1}}(θ)`.  The `r`-round exponent of the class is the least `θ` for which no `u`-Lipschitz `F` on the space
of types has more mass outside `V_{S_{r−1}}(θ)` than inside:

    τ^{(r)}(BR_m) = inf{ θ : sup_F [ max_{δ ∉ V_{S_{r−1}}(θ)} m_F(δ) − max_{δ ∈ V_{S_{r−1}}(θ)} m_F(δ) ] ≤ 0 },     m_F(δ) = −F(δ) − Σ_j φ_jf(δ_j)

(masses per coordinate, at the exponential scale; "`≥`" is Lemma U2 **[proved]**, "`≤`" needs the algorithm that
samples shell by shell and the estimate of §5.2 **[sketch]**).  This is the clean variational problem asked for in
Q3, for these classes.  What I know about its value:
* `r = 1`: `a` (flat histogram against its truncation; Theorems 11.44/11.45).
* `r = 2`, two blocks: at least `ϑ(φ₁) := min{φ₂a, root of Ξ(·,φ₁)}` (Theorem U3) **[proved]**, and at least the same
  with the blocks exchanged.  *Upper bound* **[sketch]**: for any `F` whose block-1 centre is revealed in round 1 and
  any hidden type `(x, y)`, the Lipschitz condition from the anchors `(z, ρ^s(z)) ∈ V_∅(θ)`, where `F = G(z)` does not
  depend on the second block and `−G(z) − φ₁f(z) ≤ A_v` (the visible maximum), gives
  `m_F(x,y) ≤ A_v + min_z[φ₁(f(z) − f(x)) + uφ₁|x−z| + φ₂(uρ^s(z) − Λ₁)]`, whose supremum over `x` is `Ξ(θ,φ₁)` (attained at
  `x = p_u`: this last step is numerical — the bulk of `F_D` is at `(p_u, p_u)` in all exact runs); if no centre is
  revealed in round 1 the tail lemma applies as for one cube.  So for accuracies `ε₁n`, `ε₁ → 0`, the two-round
  exponent of `BR_2(φ₁, φ₂)` should be exactly `max{h, ϑ(φ₁), ϑ(φ₂)}`.  Missing: the supremum over `x`; the case of
  both centres revealed in round 1 only on part of the shells; bounded accuracy.
* `r = 3`, two blocks: `h` **[sketch]**, §5.2.  Three blocks: the chain of §2.4 gives nothing above `h`
  **[numerical]**.
For all of `L_u` there is no such reduction: the lower bounds transfer (`BR_m ⊂ L_u`), the upper bounds do not, and
the recursion `T^{(r)}` of §1.3 is the only upper bound I have.  For two rounds the interval is
`[θ₂*, T^{(2)}(0)] = [0.359a, 0.624a]` at `u = 1`.

---

## 4. Q2 — the hierarchy, as far as it is known

**Corollary U4 [proved, given Theorems U1, U3 and Theorems 11.44, 11.45, 11.58].**  For every `u > 0`:
(a) `a = τ^{(1)} > T^{(2)}(0) ≥ τ^{(2)} ≥ θ₂*(u) > h = lim_{r→∞} τ^{(r)}`; so the sequence `(τ^{(r)})_r` takes at least three
distinct values, and there is `r₀ = r₀(u)` with `τ^{(r₀)} < τ^{(2)}`.
(b) `τ^{(r)}` is nonincreasing, `h ≤ τ^{(r)} ≤ T^{(r)}(0)`.
(c) **[numerical, for the value of `r₀`]** at `u = 1`: `T^{(48)}(0) ≤ 0.342a < 0.359a = θ₂*`, so `τ^{(48)} < τ^{(2)}`; in the
small-slope limit `T^{(32)}(0) ≤ 0.341a < 0.346a`.
*Not known:* whether `τ^{(3)} < τ^{(2)}` (`T^{(3)}(0) = 0.541a` is above `θ₂*`); whether `τ^{(r)} > h` for any `r ≥ 3`;
whether the sequence is strictly decreasing.  If `τ^{(r)} > h` for every `r`, then, since `τ^{(r)} ↓ h`, it has infinitely
many strict decreases; I could not prove the hypothesis and the most natural attempt fails (§2.4).

---

## 5. Q4 — radial and structured instances

### 5.1 Radial instances need exactly two rounds

**Proposition U9 [proved, from Theorem 11.51 [known: statement and proof read in full, `H_REPORT.md` §2.5 and theory
report §11.18]].**  On the radial class `R_u`: `τ^{(1)}(R_u) = a` and `τ^{(2)}(R_u) = h = τ^{(∞)}(R_u)`, at every bounded
accuracy.
*Proof.*  One round: the pairs "cone, truncated cone" of Theorem 11.45 are radial.  Two rounds: algorithm RAD of
Theorem 11.51 asks `M` uniform points with their `n` neighbours (batch 1), then, if some point has two distinct
neighbour values, a monotone path of `n+1` points from the centre candidate (batch 2), and otherwise answers from
batch 1 alone.  Its cost bound `(n+1)⌈ln(2n/δ)2ⁿ/C(n,r_ε)⌉ + 2n + 1` has the exponent `h` at a bounded accuracy
(`r_ε = k*(ε) − O(1 + 1/u)`, and the side condition `4|B(n, r_ε−2)|/2ⁿ ≤ δ` holds for large `n`).  ∎
Own check (`small_cube_checks.py`, part 3): RAD in two batches on `Q_14`, 300 random radial instances of five
kinds: 126 runs took the second batch and returned `ln A` exactly; 174 stopped after the first batch (flat and
2-periodic profiles, dips that were not hit), their answers within `1` of `ln A` — at this size the bracket of the
theorem is not small, so this part checks the round count and the logic, not the accuracy.

### 5.2 A class between radial and `L_u`: two rounds are not enough, three are

**Proposition U10.**  Let `BR_2 = BR_2(φ₁, φ₂) ⊃ R_u` be the class of block-radial functions on two known blocks.
(a) **[proved]** `τ^{(2)}(BR_2) ≥ max{ϑ(φ₁), ϑ(φ₂)} > h` whenever `φ₁ < 1 − h/a` or `φ₂ < 1 − h/a` — for `u ≤ 6`, where
`h/a < ½`, that is every split — (Theorem U3: its twins are members of `BR_2`), e.g. `≥ 0.359a = 1.37h` at `u = 1`,
`φ₁ = 0.64`.
(b) **[sketch]** `τ^{(3)}(BR_2) = h`.  Algorithm (`M = poly(n)·e^{nθ}`, `θ > h`): *batch 1*: `M` uniform points with
their neighbours; a block is revealed if some point has two distinct values among its neighbours in that block
(then a centre candidate `c^j ∈ {s^j, s̄^j}` is computed as in Theorem 11.51).  *Batch 2*: for every revealed block and
every distance `d`, `M` points whose part in that block is uniform on the sphere of radius `d` around `c^j` and whose
other part is uniform, with neighbours.  *Batch 3*: if both blocks are revealed, one point of each of the
`(n₁+1)(n₂+1)` types: `F` is known and `ln A` is computed exactly.  If block 2 is still not revealed after batch 2,
then on every shell `d₁` the fibre profile `d₂ ↦ F(d₁, d₂)` is 2-periodic on the range that `M` points cover, and the
estimate of Theorem 11.51 on `Q_{n₂}` (alternating binomial sums; caps bounded by the tail lemma) gives every fibre
average up to a constant factor at the cost `e^{φ₂hn} ≤ e^{nh}`; `A = Σ_{d₁}P₁(d₁)W(d₁)`.  If nothing is revealed in
batch 1 the same argument applies in both blocks at once.  *Missing:* the two-block version of that estimate when
no block is revealed; the union bounds over the types; the constants at a bounded accuracy.
So on this class the picture is `a`, strictly between, `h` for one, two, three rounds, and the reason three
rounds suffice is the one that makes §2.4 fail: there is no third centre to find.

**No class is offered on which two rounds suffice beyond `R_u`** and the trivial extension to functions that are
radial in an unknown subset of the coordinates; any class containing `BR_2(φ₁,·)` for some `φ₁ < 1 − h/a` needs three.

---

## 6. Failed attempts and traps (recorded)

1. **Nested balls / cylinders / cones (observation (iii)).**  Three families — balls inside plateaus in one cube;
   "concentric" balls in growing sets of blocks; max–min nests of cones — give no two-round bound above `h` (§3.2,
   §3.3).  Hand computations with these families produced, twice, instances that seemed to cost a fully adaptive
   algorithm more than `e^{nh}`; both times the mass of an intermediate structure had been computed additively
   where the max-structure erodes it.  The test "`r = ∞` must give at most `h`, `r = 1` at most `a`" caught both, as
   D45 says it would.
2. **The product formula for intersections of balls** with independent centres, used outside its range (`u = 4`):
   caught by the one-round necessary condition (§3.3).
3. **First version of the two-round twins** (lower McShane envelope without the cap `g₁ + g₂`): the exact computation
   plateaued at `E ≈ 1.18h` instead of approaching the predicted `1.37h`.  Cause: below the range that round 1 sees,
   the block-1 profile continued as a full cone, whose bulk `(p_u, typical)` is *visible* to round 2 and heavier than
   the typical type, so the visible maximum was not `0`.  The asymptotic analysis had silently assumed a flat
   histogram on all shells; the exact computation (`diag_lb2.py`, last columns) showed `ln A(F_S)/n ≈ 0.007` instead
   of `0`.  Repair: the cap.  *Lesson (again): compute the visible maximum, do not assume it.*
4. **A three-round family** by iterating the construction: no gain at budget `e^{nh}` (§2.4).
5. **Harness bug**: my first implementation of the sequential loop advanced a point by two rungs in one pass
   without re-testing it and thereby "violated" Claim A twice in 40 runs (§1.4).
6. **A numerical convenience that was wrong**: `p₁ = 1 − Σ_{W₁}P` in floating point is `0` or negative from `n ≈ 1600`
   on; all tail probabilities are now summed in log space over the complement.

---

## 7. Prior art (search log; generic queries only)

Everything below is from search-engine summaries of abstracts (25 Nov 2026); I read no paper in full.

| query | found | what it says, as far as read |
|---|---|---|
| adaptivity hierarchy theorem, rounds of adaptivity, query complexity | Canonne–Gur, *An adaptivity hierarchy theorem for property testing* (CCC 2017); pointer-chasing lower bounds going back to Nisan–Wigderson | for every `k` a property testable with `Õ(k)` queries in `k` rounds that needs `Ω̃(n/k²)` queries in `k−1` rounds: a strict hierarchy at every level, with polynomial-versus-linear gaps; hard instances are pointer-chasing-like |
| parallel query complexity of non-smooth convex optimisation | Nemirovski (1994); Balkanski–Singer (arXiv 1808.03880); Bubeck et al. (arXiv 1906.10655); Diakonikolas–Guzmán (arXiv 1811.01903) | with `poly(d)` queries per round, `õ(d^{1/3})` (later `Õ(√d)`) rounds do not beat one query per round; hard instance: a maximum of linear functions with offsets, each round revealing one new direction |
| batched / round-limited normalising-constant estimation | Cai–Scarlett, *Kernelized normalizing constant estimation* (arXiv 2401.05716); Mathé–Novak (arXiv math/0611285) | a two-batch algorithm with matching lower bounds in an RKHS setting (no round lower bound seen in the summary); Mathé–Novak: non-adaptive versus adaptive for log-concave densities, no round count |
| limited rounds of adaptivity, batched bandits | Agarwal et al. (COLT 2017); Gao–Han–Ren–Zhou (arXiv 1904.01763) | `Θ(log* n)` rounds necessary and sufficient for optimal query complexity in top-`k` coin identification; batch–regret trade-offs |
| adaptive sparse recovery with limited adaptivity | Price–Woodruff (arXiv 1205.3518); Kamath–Price | `Θ(k·log^{1/R} n)` measurements with `R` rounds (up to `log* k`): a smooth round–cost trade-off |
| adaption versus non-adaption in information-based complexity | Novak (survey, arXiv 2307.06787); Heinrich; Kunsch–Novak–Wnuk (arXiv 2308.01705) | adaption helps for some randomised linear problems by polynomial factors; nothing on the number of adaptive stages in the summaries |

Relation to this report.  The max–min nests of §3.3 are the cube version of the Nemirovski construction, and the
additive jump costs there are the pointer-chasing mechanism; here they do **not** give a round lower bound, because a
batch of `e^{nh}` points is allowed and finds several levels at once.  What separates two rounds from many here — a
flat histogram that dilutes the first batch — I did not find in these summaries; "not found", not "new".  Trade-offs
of the kind "exponent as a function of the number of rounds" (sparse recovery, bandits) are the closest in form;
the present one has a finite limit `h` and, as far as I can prove, only one non-trivial step.

---

## 8. Conjectures, open questions, and what I did not check

**Conjectural / open.**
1. `τ^{(3)} = h`?  (Three rounds suffice on `BR_2` **[sketch]**; the three-block chain hides nothing **[numerical]**;
   no three-round algorithm for `L_u` better than `T^{(3)}(0) = 0.541a`.)  Either answer would be new: a
   three-round algorithm reaching `h` on all of `L_u` would have to use local information (slopes), which the
   nested algorithms never do; a three-round lower bound needs a family that is not a chain of blocks.
2. The value of `τ^{(2)}` in `[θ₂*, T^{(2)}(0)]`.  **[conjecture]** `τ^{(2)}(BR_2(φ₁,φ₂)) = max{h, ϑ(φ₁), ϑ(φ₂)}` at vanishing
   extensive accuracy (§3.4).  For `L_u` I have no conjecture: the lower bound could increase if the first-round
   structure were not radial (so that knowing it after round 1 does not give access to all its shells), the upper
   bound could decrease with an algorithm that samples around the best points of round 1.
3. Strict monotonicity of `τ^{(r)}`, and the rate of `τ^{(r)} → h` (upper bounds only).

**Not checked.**
* Theorem U1 rests on Theorem 11.56 (refereed, R8), which I read but did not re-derive; the harness uses a simulated
  inner oracle, small outer cubes (`n_o ≤ 10`), reduced `K`, and exercises no nested levels and no real inner
  brackets.  Corollary U1.1 repeats the assembly of `K_REPORT.md` (Propositions E, K5) with round counts; I did not
  write the induction out again.
* The cost of the two-round algorithm (Corollary U1.2) at finite `n` was not evaluated; its exponent formula is that
  of Proposition 11.57(b), whose finite-`n` behaviour at the flat instance is in `K_REPORT.md` §6.4 (for the
  sequential schedule).  The batched schedule calls rung 1 on all `M_max` points, which changes polynomial factors.
* The numbers `T^{(r)}(0)` come from a grid recursion with conservative rounding (`K = 120` accuracy levels, 79
  values of `φ`, 24 tolerances); they are upper bounds for the recursion, not its exact values (the exact two-round
  value is `0.6243a` against `0.6254a` from the grid at `u = 1`).  For `r ≥ 24` at `u = 1` only some round numbers were
  allowed for the inner procedures.
* Theorem U3: the asymptotic proof is on paper; the finite-`n` statements are exact computations for the listed
  `n`, `u ∈ {1, 2}`, accuracy `1`, and a grid of five or six values of `n₁/n` (not optimised further).  The optimal
  `φ₁` and `θ₂*` are numerical roots.  Extension to expected batch sizes: only the Markov remark.
* §2.4 (three rounds): small-slope limit only; one family; grids of at most 241 points per coordinate.
* §3.3: an idealised game (centres revealed by a hit), random search, at most four levels; the erosion inequality
  is proved only in the case described.
* §3.4 and Proposition U10(b): sketches, as labelled.
* Prior art: search summaries only.
* No Lean; nothing here is machine-checked.

---

## 9. Scripts, commands, sizes, run times

All in `scratchpad/ws/U/code/`, run from that directory as `ulimit -v 4000000; python3 <script> <args>`; outputs in
`scratchpad/ws/U/out/`.  Python 3 with numpy 2.5.3 and scipy 1.18.1; seeds are fixed in the scripts (`20261125`
unless given).  Times are wall-clock on the 4-core container, one process at a time.

| script (args) | what | sizes | time | output |
|---|---|---|---|---|
| `ulib.py` | shared formulas (`f`, `f^{-1}`, `θ_na`, `θ_hint`, `D`, `x_na`, binomial tables) | – | – | – |
| `ub2_closed.py` | Corollary U1.2: direct minimisation of the two-round bound, `u → 0, 0.5, 1, 2, 3`; `θ₂*` again | 4000 × 2001 × 61 grid | 1 m 56 s | `ub2_closed.txt` |
| `ub_rounds.py gauss 2,3,4,5,6,7,8,10,12,16,24,32 120` | recursion `T^{(r)}`, small-slope limit | 121 accuracies × 79 `φ` × ≤ 24 tolerances | 3 m 19 s | `ub_rounds_gauss.txt` |
| `ub_rounds.py 1.0 2,3,4,5,6,8,12,16,24,32 120` | the same at `u = 1` | as above | 2 m 34 s | `ub_rounds_u1.txt` |
| `ub_rounds.py 1.0 2,3,4,6,8,12,16,24,32,48,64 120` | `u = 1` up to 64 rounds | as above | 6 m 11 s | `ub_rounds_u1_r64.txt` |
| `batched_ladder_sim.py 150 20261125 1.0` | harness for Theorem U1 (Claims A, B; two mutations) | 150 runs × 3, `n_o ≤ 10`, ≤ `4·10⁶` outer points per run | 2 m 10 s | `batched_ladder_sim_u1.txt` |
| `batched_ladder_sim.py 100 7 3.0` | the same, `u = 3`, seed 7 | 100 runs × 3 | 3 m 09 s | `batched_ladder_sim_u3.txt` |
| `lb2_exponent.py` | `Ξ`, `θ₂*` for the small-slope limit and `u = 0.25 … 6` | 86 + 41 values of `φ₁` per `u` | 6 m 54 s | `lb2_exponent.txt` |
| `lb2_exact.py 1.0 1.0 1 200 400 800 1600 3200 6400 12800` | exact twins of Theorem U3, `u = 1`, gap `> 1` | type grids up to `7681 × 5121`; 14–20 bisection steps × 3–6 splits | 3 m 07 s | `lb2_exact_u1_cap.txt` |
| `lb2_exact.py 2.0 1.0 1 200 400 800 1600 3200 6400` | the same, `u = 2` | up to `3585 × 2817` | 49 s | `lb2_exact_u2_cap.txt` |
| `lb2_exact.py 1.0 1.0 0 400 800 1600 3200 6400` | record of the first version without the cap (§6, item 3) | as above | 53 s | `lb2_exact_u1_nocap.txt` |
| `diag_lb2.py 0.6` | asymptotic formula of Theorem U3 against exact values; capped and uncapped | `n = 1600, 6400, 12 800`, four budgets | 27 s | `diag_lb2.txt` |
| `small_cube_checks.py` | twins on whole cubes `Q_12`–`Q_16`; Lemma U2 by simulation; RAD in two rounds on `Q_14` | 5 cubes; 5 × 4000 trials; 300 instances | 2 s | `small_cube_checks.txt` |
| `lbr_gauss.py 161` | `Ξ₂`, `Ξ₃` in the small-slope limit; search for a three-round bound | grids 81–241 | 1 s | `lbr_gauss.txt` |
| `scan_xi3.py` | `Ξ₃(h)` for small `φ₁`; largest `θ` with `Ξ₃ > 0` | 7 × 8 splits; 8 × 16 splits | 15 s | `scan_xi3.txt` |
| `lbr_gauss_bruteforce.py` | independent brute-force construction for `r = 2, 3` | grids `400²`, `90³` | 2 s | `lbr_gauss_bruteforce.txt` |
| `cond_cover.py` | Proposition U6 by exact counting | `n ≤ 3200`, 7 pairs | 3 s | `cond_cover.txt` |
| `explore_gauss_on2.py 4` | §3.3: nests of cones, small-slope limit (exploration) | 11 patterns × ≤ 4 rounds, `1.2·10⁵` instances × 10 | 6 m 06 s | `explore_gauss_on2.txt` |
| `explore_onu.py 1.0 3`, `explore_onu.py 4.0 3` | §3.3 at `u = 1`; the trap at `u = 4` | 6 patterns, `10⁵` instances × 10 | 6 m 41 s, 6 m 49 s | `explore_onu_u1.txt`, `explore_onu_u4.txt` |

The exploration scripts (`explore_*`) are records of the negative results of §3.3 and are evidence only for what
is said there.
