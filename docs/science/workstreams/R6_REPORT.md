# R6 — Independent line-by-line review of the cost of the nested adaptive ("layer-cake") algorithm

Object: theory report `docs/THEORY_REPORT.md` §§11.18–11.19 (Theorems 11.52, 11.54, 11.56, Proposition
11.57, Theorem 11.58) and `docs/workstreams/H_REPORT.md`, `docs/workstreams/K_REPORT.md`, read at commit
**`5ed4072`** (the commit of this branch's theory files).  One addition published by the theory division
while I worked — the remark "the sample-size cap can be lowered" after Theorem 11.56, commit
**`40c5bd7`** — is reviewed in §2.8.  Every finding below carries the commit it refers to; where
nothing is said it is `5ed4072`.

Workstream directory: `experiments/science/ws_R6/` (scripts, data, logs, `NOTES.md` with the order in
which things were done).  Nothing outside that directory and this file was written; no state-changing
git command; no `lake build`; nothing delegated.

## 0. How far I got (read this first)

* **Re-derived on my own paper, before reading the authors' proof** (`NOTES.md`, Steps 2 and 4): the whole
  of Theorem 11.52 — good event, validity of both ends, width, termination, sample sizes, the count of
  points near a level, the cost sum and its exponent; and, from the *statement* of Theorem 11.56 alone,
  the width, the closing radius, the sample sizes and the count of Algorithm 2L⁺.  I then read the
  authors' proofs (theory report lines 3654–3716; `K_REPORT.md` §2.4, Steps 1–9) and compared term by
  term (§2.4 below): **my constants and theirs coincide in every term**.
* **Re-derived after reading**: `K_REPORT.md` Steps 1–3, 8, 9 (classification, certificates, validity,
  cost, termination), the probability of the good event, Lemma K.4 = 11.55 (a)–(d), Proposition K0 =
  11.57(a), Corollary K1.b, Proposition E, Theorem K2 = 11.57(b) (including the uniform version),
  Proposition 11.57(c), the iteration of Theorem K3 = 11.58, the assembly of Theorem 11.54 with left
  limits (shift and induction), the two tail lemmas (given Harper's theorem), and the cap remark of
  `40c5bd7`.
* **Only read, not re-derived**: the *proofs* inside the Lean files (I read the statements against the
  paper, compiled them and printed their axioms); the proof of Theorem 11.53(c)–(d) on paper (it is
  machine-checked); Theorems 11.25, 11.44, 11.45 beyond the statements used; Theorem 11.51;
  Proposition K5(d) (numerics of the recursion); Harper's theorem, the Chernoff/Hoeffding bounds and
  the binomial-median fact (cited facts; I checked the first and the last by computation, §3.5).
* **Own implementation** (written from the specification before any implementation of the authors,
  their referees or the engineering division was opened; I have still not read any of them):
  Algorithm 2L and Algorithm 2L⁺ with every constant of the theorems, a run-by-run checker of every
  claim, and an explicit evaluator of the cost bound for every `n` (§3).
* **Done only at toy size**: runs with real inner brackets — two levels on cubes of 12–13 coordinates
  (529 runs), three nested levels on cubes of 9–10 coordinates (19 outer runs); they test the logic of
  the nesting, not the cost (§3.4, §5).
* **Not done**: a run with real inner brackets at sizes where sampling is cheaper than enumeration
  (not feasible with the constants of the theorems: §5); Theorem 11.51; a second reading of the lower
  bound's asymptotics; the Lean proofs line by line.

## 1. Verdicts in one paragraph

**The cost accounting of the nested algorithm stands.**  I found no critical and no major error in
Theorems 11.52, 11.54, 11.56, Proposition 11.57 and Theorem 11.58: an accounting written from scratch
reproduces the published one constant by constant (the closing radius, `M ≤ 8Je²M†` resp. `M̄`, the
count `16KJe²e^x` resp. `c_η⁻¹e^λνe^x` in which the two factors `e^b` cancel, the per-rung call
bound); the five wrong accountings of `DEAD_ENDS.md` D45 are not repeated in another guise (§2.5); an
independent implementation violated no claim in **3,686 literal runs** of Algorithms 2L⁺ and 2L with a
simulated inner oracle — 2,618 with the constants of the theorems and valid inner answers (the events
of the proof never failed, every bracket was valid), 264 with `K` reduced (events fail, claims hold
whenever they hold), and, for the first time, **804 runs with invalid inner answers** (the statements
"for every run, on or off the good event" hold in all of them; with a dear last rung 149 of 260 such
runs would exceed `C_max` without the abort rule, and none does with it) — nor in 529 two-level and
19 three-level runs with real inner brackets at toy size, nor in 4,500 runs aimed at the degenerate
branch of the new cap remark and 2,425 runs of two searches for a counterexample (§3); and it
reproduces to every published digit numbers of the engineering division that I had not seen when I
wrote it (§3.3).  **What I add:** (i) seven minor
points, each with its repair (§2.7): four gaps in the text of §11.18, an uncovered pass in the proof of
the new cap remark of `40c5bd7`, which I close (§2.8), and two observations; (ii) an **every-`n` statement
with no `o(n)`**: the two-level algorithm
with base brackets has an explicit worst-case cost bound for every `n` on the whole class, and at
`u = 1`, accuracy `0.872`, `δ = 0.05` that bound is **below the lower bound for all non-adaptive
algorithms from `n = 1400` on** (`n = 540` for `u = 2`, `n = 4700` for `u = ½`; §2.9) — a finite-`n`,
fully explicit separation that none of the reports states; (iii) a precise list of what is and is
not machine-checked (§2.6).  **What remains true about the weakness of the result:** the exponent `h`
is reached only in the limit of many nested levels, as "for every `η > 0` there is a family with
exponent `≤ h + 2η`"; the `o(n)` is not quantified; nothing in the count of evaluations is
machine-checked; and no run of three or more levels exists at a size where the levels do anything but
enumerate.

| statement (commit `5ed4072` unless stated) | verdict | basis |
|---|---|---|
| Theorem 11.52 (one more level; Algorithm 2L) | **proved** (four minor gaps, all closed: m1–m4) | own derivation before reading; 347 own runs of 2L |
| Theorem 11.53 (recursion → hinted exponent) | **[V]**: statement read against the paper, compiled, axioms printed | `lean/R6Axioms.lean`; the Lean *proof* not read |
| Theorem 11.54 (extensive accuracies) | **proved**, given 11.25(a) [V], 11.53 [V], 11.44/Prop. 11.46 or K0 [P], Harper, Chernoff [K] | assembly re-derived in both forms (left limits; Proposition E) |
| Lemma 11.55 = K.4 | **proved**, given the binomial median [K] | re-derived; exact tables `m ≤ 4000` |
| Theorem 11.56 = K1 (Algorithm 2L⁺) | **proved** | Steps 4–7 derived before reading, 1–3, 8, 9 after; 3,339 own simulated-oracle runs, 529 with real inner brackets |
| Remark after 11.56, "cap `2max{e^λM†, M‡}`" (**`40c5bd7`**) | **proved with a gap that I close** (m7) | re-derived; checked in every run |
| Proposition 11.57(a) = K0 | **proved** | re-derived; cost reproduced numerically for `d ≤ 16 000` |
| Proposition 11.57(b) = K2, (c) | **proved** (in the corrected form `T′(ξ) = min(T(ξ), T′(0))`) | re-derived, including accuracy arithmetic and (E0′) |
| Theorem 11.58 = K3, Corollary K3′ | **proved**, given the above, 11.25(a),(d) and (R) = `exactRec_reaches_hint` [V] | iteration re-derived; `two_rung_bound` [V] |
| Theorem 11.51 (radial class) | not examined | — |

## 2. Precise statements, proofs, findings

Labels: **[V]** machine-checked (the Lean declaration is named), **[P]** paper proof (theirs, re-derived by
me, or mine; I say which), **[K]** known and cited (with the reading level in §4), **[N]** numerical evidence
(everything in §3 unless a declaration is named), **[H]** heuristic.  "Re-derived" means: written out by me
independently; "replicated" means: re-computed with my own code.

Notation (theory report §11.16/§11.18): `Q_n` the cube; `L_u(Q_n)` the functions with
`|ψ(x) − ψ(y)| ≤ u·d_H(x,y)`; `w = e^{−ψ}`, `A = 2^{−n}Σ_x w(x)`; `p_u = 1/(1+e^u)`,
`Λ₁ = ln(2/(1+e^{−u}))`, `ε* = ln cosh(u/2)`, `a = KL(p_u‖½)`, `h = KL(Λ₁/u‖½)`;
`θ_na(e) = min{KL(ρ‖½) : KL(ρ‖p_u) ≤ e}`, `θ_hint(e) = KL((Λ₁+e)/u‖½)`; on a cube `Q_m`:
`B(m,r)` the Hamming ball, `E_r(m) = Σ_{j≤r}C(m,j)(e^{u(r+1−j)} − 1)`, `T_m(k) = Σ_j C(m,j)e^{−u(j−k)₊}`,
`Γ̃(r) = E_r(m)/|B(m,r−1)|` (`Γ̃(0) = e^u − 1`).  Split `Q_n = Q_{n_o} × Q_{n_i}`, fibre averages
`W(a) = 2^{−n_i}Σ_b e^{−ψ(a,b)}`, `A = E_a W(a)`, `p(s) = P_a(W(a) > s)`.

### 2.1 The algorithm as I understand it

**Bracket procedure** (theory report lines 3591–3601; `K_REPORT.md` §1.3).  For dimension `d`, accuracy
`x`, failure probability `δ′`, cost `C`: a randomised adaptive algorithm that makes at most `C` queries
to **any** `ψ ∈ L_u(Q_d)` in **every** run, and returns `L ≤ U` such that, except with probability `δ′`
(over its own randomness, for each fixed `ψ`), `L ≤ A(ψ) ≤ U` **and** `U ≤ e^xL`.  A *family* has one
procedure for every `(d, x, δ′)` with cost nonincreasing in `x` and in `δ′`; it has the *exponent
function* `T` if `limsup_d d⁻¹ ln C(d, ξd, e^{−cd}) ≤ T(ξ)` for every `ξ > 0`, `c > 0` (E1), and the
exponent `T(0)` *at bounded accuracy* if `limsup_d d⁻¹ ln C(d, x, e^{−cd}) ≤ T(0)` for every fixed
`x > 0`, `c > 0` (E0).  Two base families: one query (accuracy `2ud`), and the two-sample bracket.

**Algorithm 2L** (Theorem 11.52; theory report lines 3616–3652).  *Input:* oracle access to
`ψ ∈ L_u(Q_n)`; `0 < φ < 1`, `0 < β < g`, `η₀ > 0`, `δ`; an inner family.  *Constants:* `n_o = ⌊φn⌋`,
`n_i = n − n_o`; `G = gn`; ladder `x_l = ξ_l n_i` with fixed rates `2u = ξ₀ > ξ₁ > … > ξ_last = β/(1−φ)`,
steps `≤ η₀`; tolerance `b := x_last`; `K = ⌈24 ln(2^{n+6}n³/δ)⌉`; `J = ⌈2un + b + n_o ln 2 + 10⌉`;
inner failure probability `δ/(2^{n+6}n³)`.  *State:* levels `s_j = s₀e^j`, `s₀ = e^{−ψ(ref)−un}` (one
query; `s₀ ≤ W ≤ s₀e^{2un}`); a certified lower bound `ℓ` (initially `s₀`); a list `a₁, a₂, …` of
i.i.d. uniform outer points, each with a bracket `[L_i, U_i]` of `W(a_i)` that is only ever refined
(rung 0: one query on the fibre, ratio `e^{2un_i}`; rung `l`: the inner procedure at accuracy `x_l`,
intersected); the values `q_i` of the levels already left.  *What is random:* the outer points and the
inner procedures' randomness; the levels are functions of the reference value only.
*Classify `a_i` at level `j`:* refine until `U_i ≤ s_j` (low) or `L_i > s_je^{−b}` (high).
*Level `j = 0, 1, …`:* `M := K`; repeat — classify `a₁..a_M`; `N := #high`; `q := min(1, 2max(N,K)/M)`;
if `N ≥ K`: `ℓ := max(ℓ, s_je^{−b}N/(2M))`; **closure test:** `r :=` least radius with
`|B(n_o,r)| ≥ 2^{n_o}q`; if `r = n_o` no closure; else `tail := s_j2^{−n_o}E_r(n_o)` (`0` if `2^{n_o}q < 1`),
and if `tail ≤ e^Gℓ` **stop**, returning `[ℓ, s₀ + Σ_{i<j}s_{i+1}q_i + tail]`; otherwise, if `N ≥ K`
(*populated*) or `M ≥ M_j^neg := 2KJe·s_j/(ℓe^b)` (*negligible*): `q_j := q`, next level; else `M := 2M`.
*Abort* (trivial bracket `[s₀, s₀e^{2un}]`): the query count exceeds the bound of the cost proof, or
level `J + 1` is reached, or a point is unclassified at `x_last`.

**Algorithm 2L⁺** (Theorem 11.56; complete text `K_REPORT.md` §2.2, lines 207–246).  Parameters
`0 < λ ≤ 1`, `0 < η ≤ ½`, `0 < η′ ≤ 1`, `θ > 0`, `ν₁ ≥ 1`, tolerance `b`, `δ`, ladder
`2un_i = x₀ > x₁ > … > x_L`, `x_L ≤ b`, inner procedures `I_l` of accuracy `x_l`, failure probability `δ′`,
cost `C_l`.  Constants, in the order in which they can be computed (no circularity):

    J = ⌈(2un + b + n_o ln 2)/λ⌉ ,   ν₀ = (1−η)⁻¹ max{(J+1)(e^λ − 1)/η′, ν₁} ,   c_η = (1−η)/(1+η) ,
    r† = largest r ≤ n_o − 1 with  [N] Γ̃(r′) ≤ θ(1−η)ν₀  and  [P] min{Γ̃(r′)/c_η, Γ″(r′)} ≤ θ  for all r′ ≤ r ,
         Γ″(r) = E_r(n_o)/T_{n_o}(κ(r)),  κ(r) = largest k with |B(n_o,k)| ≤ max{1, c_η|B(n_o,r−1)|} ,
    π† = 2^{−n_o}|B(n_o, r†)| ,   m_max = ⌈log₂(2(1+η)e^λν₀/((1−η)π†))⌉ ,
    K = ⌈3(1+η)η⁻² ln(2(J+1)(m_max+1)(L+2)/δ)⌉ ,   ν = Kν₀ ,   M† = K/((1−η)π†) ,   M̄ = 2(1+η)e^λν₀M† ,
    δ′ = δ/(4LM̄) ,   cnt(x) = max{K, 2(1+η)²(1−η)⁻¹e^λ·ν·e^x} ,
    C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{2M̄, (J+1)cnt(x_{l−1})}·C_l .

Differences from 2L: levels `s_j = s₀e^{jλ}`; `ℓ` starts at `e^{−ψ₀}((1+e^{−u})/2)^n` (`= (2p_u)^{−n}s₀`);
`q := min{1, max(N,K)/((1−η)M)}`; at a populated pass `p̲ := N/((1+η)M)`, `k :=` largest radius with
`|B(n_o,k)| ≤ max{1, 2^{n_o}p̲}`, and `ℓ := max{ℓ, s_je^{−b}p̲, s_je^{−b}2^{−n_o}T_{n_o}(k)}` (the last is the
*Harper term*); closure test `tail ≤ θe^bℓ` with `tail = +∞` if `r = n_o`; returned pair
`L = max{ℓ, Σ + [N≥K](1−e^{−λ})e^{−b}s_jp̲}`, `U = s₀ + Σ_{i<j}(s_{i+1} − s_i)q_i + tail`, where
`Σ = Σ_{populated i<j}(1−e^{−λ})e^{−b}s_ip̲_i`; negligibility threshold `M_j^neg = ν s_j/(ℓe^b)` with the
value of `ℓ` at the entry of the level; abort if a point is unclassified at rung `L`, if `M` would
exceed `K2^{m_max}`, if level `J` is left, or if an inner call would take the number of queries beyond
`C_max` (tested *before* the call; a pair with `L > U` is replaced by the trivial bracket).

What is *stored*: per outer point one bracket and its rung; per level left `q_i` (and `p̲_i`); `ℓ`, `Σ`.
What an inner call is allowed to do: anything, as long as its number of queries is at most `C_l`; the
proof needs its answer to be valid and of ratio `≤ e^{x_l}` only on the good event.

### 2.2 The statements, with their quantifiers

* **Theorem 11.52.**  *For every* inner family with nonincreasing exponent function `T`, *every*
  `0 < φ < 1`, `0 < β < g`, `η₀ > 0`: there are procedures (one per `n` and `δ`) with accuracy
  `gn + O(log n)` (precisely `ln(1 + 4Je^{b+1} + e^b + e^G) ≤ gn + ln(4eJ+3)` when `b ≤ G`) such that *for
  every* `c > 0`, with `δ = e^{−cn}`: validity and width hold with probability `≥ 1 − δ` **for every
  `ψ ∈ L_u(Q_n)`** (for `n ≥ n₀(η₀)`), and the number of queries is at most `exp(n(τ + η₀) + o(n))` **in
  every run** (by the abort rule), `τ = sup_{γ≥β}[min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ))]` (11.18.2).
  The `o(n)` hides: the polynomial factors `K, J, 1/η₀`; the Stirling error in
  `M† = e^{nφθ_na((g−β)/φ)+o(n)}`; the finitely many `o(n_i)` of the inner family at the rates `ξ_l`.
  It depends on `(u, φ, β, g, η₀, c)` and on the inner family, not on `ψ`.
* **Theorem 11.54.**  *For every* `u > 0`, `0 < ε₁ < ε*`, `0 < δ < ½`: `min_alg max_{ψ∈L_u(Q_n)} #queries
  = exp(nθ_hint(ε₁) + o(n))`, accuracy `ε = ε₁n` (*extensive*), correctness "`|output − ln A| ≤ ε/2` with
  probability `≥ 1 − δ` for every member".  Upper bound: a deterministic bound on the queries in every
  run; lower bound: expected queries at the zero function.  The upper bound is: *for every* `η > 0`
  there is a `k = k(ε₁, η)` and a `k`-level family with cost `exp(n(θ_hint(ε₁) + η) + o_η(n))`.
* **Theorem 11.56.**  *For every* `n ≥ 2`, `1 ≤ n_o ≤ n−1` and all parameters as above — **no
  asymptotics** — Algorithm 2L⁺ is a bracket procedure with accuracy
  `x_out = ln[(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)]`, failure probability `δ`, cost `C_max`.  On an event
  of probability `≥ 1 − δ`: no abort, every certificate true, the count holds; **in every run**: closing
  radius `> r†` at every level left, `M ≤ M̄`, and the width whenever the run stops through the test.
* **Proposition 11.57.**  (a) the two-sample bracket closed by both tail lemmas has ratio
  `≤ ((1+η)/(1−η))(1 + Γ″(r̂))` and cost `exp(d·a + O(√d))` at every fixed accuracy, `T₁ = θ_na` on `(0,∞)`;
  (b) from a family with exponent function `T` on `[0,∞)` one more level gives, at bounded accuracy,
  `T′(0) ≤ max{φa, max_{l<L}[min(φa,(1−φ)ξ_{l−1}) + (1−φ)T(ξ_l)], min(φa,(1−φ)ξ_{L−1}) + (1−φ)T(0)}`, uniformly
  for accuracies `x_n → 0` with `ln(1/x_n) = o(n)`; (c) no level undercuts `h`.
* **Theorem 11.58.**  *For every* `u > 0`, fixed `ε > 0` (and every sequence `ε_n = o(n)` with
  `ln(1/ε_n) = o(n)`), `0 < δ < ½`: `min_alg max_ψ #queries = exp(nh + o(n))`, in the worst case and
  likewise in expectation (the upper bound is deterministic, the lower bound is on the expectation at
  one instance, so both statements follow).

### 2.3 My accounting (written before reading theirs)

Written out in `NOTES.md` Step 2 for Algorithm 2L; reproduced here because it is the object of the
brief.  **[P; every inequality below was afterwards checked on every run of my implementation, §3.]**

*Facts that use no probability* (any outer points, any inner answers, valid or not):

(D1) `M` is doubled only at a pass that is unpopulated, not closed, and has `M < M_j^neg`; `ℓ` does not
change at such a pass.  So every sample of level `j` is `K` or `< 2M_j^neg(ℓ_j)`, `ℓ_j` the value at entry.

(D2) A level left as populated has `s_{i+1}q_i ≤ e·s_i·2N/M = 4e^{b+1}·s_ie^{−b}N/(2M) ≤ 4e^{b+1}ℓ`; a level
left as negligible has `s_{i+1}q_i ≤ e s_i·2K/M_i^neg = e^bℓ/J`.  With `s₀ ≤ ℓ`, `tail ≤ e^Gℓ` and at most
`J` levels left before the closing one: `U/ℓ ≤ 1 + 4Je^{b+1} + e^b + e^G`, hence the width.

(D3) *Closing radius.*  Let `r*` be the largest `r ≤ n_o − 1` with `Γ̃(r′) ≤ e^{G−b}/4` for all `r′ ≤ r`,
`π* = 2^{−n_o}|B(n_o, r*)|`.  If a level is left without closure, then `q > π*`.  Proof: by minimality of
`r = r(q)`, `2^{−n_o}E_r ≤ qΓ̃(r)` (for `r = 0` because `2^{n_o}q ≥ 1`).  Populated: `ℓ ≥ s_je^{−b}q/4`, so
`tail ≤ 4e^bℓΓ̃(r)`, and no closure forces `Γ̃(r) > e^{G−b}/4`.  Negligible: `q ≤ 2K/M ≤ ℓe^b/(Jes_j)`, so
`tail ≤ e^bℓΓ̃(r)/(Je)` and `Γ̃(r) > Je·e^{G−b}`.  If `r = n_o`, `r > r*` trivially.

(D4) *Sample sizes.*  After a populated level `i`: `ℓ ≥ s_ie^{−b}q_i/4 > s_ie^{−b}π*/4`, so
`M_{i+1}^neg < 8e²KJ/π*`.  After a negligible level: `M_i^neg ≤ M_i < 2K/π*` and `M_{i+1}^neg ≤ e·M_i^neg`.
Level 0: `M₀^neg = 2KJe^{1−b}`.  Hence **`M ≤ 16e²KJ/π*` at every pass of every run.**

*Good event.*  (V1) every inner answer valid and of the promised ratio; (V2) for every level `j` and
every `M ∈ {K2^t}`: if `Mp(s_j) ≥ 2K`, at least `Mp(s_j)/2` of `a₁..a_M` have `W > s_j` (fails with
probability `≤ e^{−K/4}`); (V3) for all `j`, `M`, `x ∈ b + ℕ`: at most `max(2Mp(s_je^{−x}), K/2)` of
`a₁..a_M` have `W > s_je^{−x}` (`≤ e^{−K/12}`: Chernoff if `Mp ≥ K/4`, domination otherwise).

*Validity.*  (V1) gives `#{W > s_j} ≤ N ≤ #{W > s_je^{−b}}` among the first `M`.  With (V2): `p(s_j) ≤ q`
at every pass.  With (V3) at `x = b` and `N ≥ K > K/2`: `N ≤ 2Mp(s_je^{−b})`, so
`s_je^{−b}N/(2M) ≤ s_je^{−b}p(s_je^{−b}) ≤ A` (Markov).  Upper end: layer cake
`A ≤ s₀ + Σ_{i<j}s_{i+1}p(s_i) + E(W − s_j)₊` and the tail lemma with `|{W > s_j}| ≤ 2^{n_o}q ≤ |B(n_o,r)|`,
`r ≤ n_o − 1`.

*The count.*  Let level `j` be reached, `x ∈ b + ℕ`.  If `s_je^{−x} ≥ s₀` let `i < j` be the level with
`s_i ≤ s_je^{−x} < s_{i+1}`; it was left, so on the good event `p(s_je^{−x}) ≤ p(s_i) ≤ q_i ≤ 4e^{b+1}ℓ_j/s_{i+1}`
by (D2), and by (D1) `M ≤ 4KJe·s_j/(ℓ_je^b)`: the product is

    2M_j^neg · p(s_je^{−x})  ≤  16e²KJ · s_j/s_{i+1}  ≤  16e²KJ · e^x ,

free of `ℓ_j` and of `b`.  If `s_je^{−x} < s₀`, then `p = 1` and `2M_j^neg ≤ 4KJe·e^{x−b}` because `ℓ_j ≥ s₀`.
With (V3): at most `32e²KJe^x` (or `K`) of the points used at level `j` have `W > s_je^{−x}`.

*Cost.*  A call of rung `l ≥ 1` for `a_i` at level `j` happens only if the rung-`(l−1)` bracket has
`U > s_j` and `L ≤ s_je^{−b}`; on (V1) `W ≥ L ≥ Ue^{−x_{l−1}} > s_je^{−x_{l−1}}`.  Rounding `x_{l−1}` up into
`b + ℕ` costs a factor `e`; each point is called at most once per rung in the whole run.  Hence

    #queries ≤ 1 + M̄ + Σ_{l≥1} min{ M̄ , (J+1)·32e³KJ·e^{x_{l−1}} } · C_l ,      M̄ = 16e²KJ/π* ,

with exponent `max_l[min(φθ_na((g−β)/φ), (1−φ)ξ_{l−1}) + (1−φ)T(ξ_l)] ≤ τ + η₀`.

*Termination.*  On the good event `ℓ ≤ A ≤ s₀e^{2un}`; at level `J` nothing is high and
`M_J^neg ≥ 2KJe^{11}2^{n_o}`, so the doubling reaches `M = K2^{n_o+2}`, where `2^{n_o}q < 1` and the tail is
empty.  (Deterministically, `M ≤ 4K2^{n_o}` always.)

For Algorithm 2L⁺ I derived, from the four changes listed in the statement of Theorem 11.56 and
before opening `K_REPORT.md` §2.4 (`NOTES.md` Step 4): the width
`(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)` term by term; the two conditions [N], [P] that a level left
without closure must violate (negligible: `tail ≤ e^bℓΓ̃(r)/((1−η)ν₀)`; populated: `tail ≤ e^bℓ·Γ̃(r)/c_η`
through the Markov term and `tail ≤ e^bℓ·Γ″(r)` through the Harper term, because `2^{n_o}p̲ = c_η2^{n_o}q >
c_η|B(n_o,r−1)|` gives `k ≥ κ(r)`); `M_j^neg ≤ (1+η)e^λν₀M†` and `M ≤ M̄`; and the count
`M_j^neg p(s_je^{−x}) ≤ c_η⁻¹e^λ·ν·e^x`.

*The good event of Algorithm 2L⁺ and its probability* (`K_REPORT.md` §2.4; re-derived after reading).
With `X_t(M) = #{i ≤ M : W(a_i) > t} ~ Bin(M, p(t))` and `ℳ = {K2^m : m ≤ m_max}`:
(V1) every *potential* inner call `(i, l)`, `i ≤ K2^{m_max}`, `l ≤ L`, is valid and of ratio `≤ e^{x_l}` — at most
`L·K2^{m_max} < 2LM̄` calls, each failing with probability `≤ δ′ = δ/(4LM̄)` given its fibre: total `< δ/2`;
(V2) for `j ≤ J`, `M ∈ ℳ`: `Mp(s_j) ≤ K/(1−η)` or `X_{s_j}(M) ≥ (1−η)Mp(s_j)` — each fails with probability
`≤ e^{−η²K/2}`; (V3) for `j ≤ J`, `M ∈ ℳ` and the `L + 1` thresholds `t ∈ {s_je^{−b}} ∪ {s_je^{−x_l} : l < L}`:
`X_t(M) < K` or `X_t(M) ≤ (1+η)Mp(t)` — each fails with probability `≤ e^{−η²K/(3(1+η))}` (Chernoff if
`Mp ≥ K/(1+η)`, monotonicity in `p` otherwise).  There are `(J+1)(m_max+1)(L+2)` events (V2), (V3), and
`K = ⌈3(1+η)η⁻² ln(2(J+1)(m_max+1)(L+2)/δ)⌉` makes their total `≤ δ/2`.  The thresholds are functions of
`ψ₀` alone and the list `a₁, a₂, …` is not influenced by inner answers, so these are statements about
binomial variables at fixed thresholds; the sizes actually used lie in `ℳ` because `M ≤ M̄ ≤ K2^{m_max}`
holds in every run.  Hence `P(good event) ≥ 1 − δ` for every `n`, with no "for `n` large" (unlike Theorem
11.52, whose `K` is fixed in advance and whose failure bound needs `n ≥ n₀(η₀)`).

### 2.4 Term-by-term comparison

| quantity | my accounting | theirs | location of theirs |
|---|---|---|---|
| 2L: closing radius of a level that is left | `r > r*`, i.e. `q > π*`, `Γ̃ ≤ e^{G−b}/4` | `r > r†`, `q_j > 2K/M†`, `M† = 2K/π*` | theory report 3677–3681 |
| 2L: threshold after a populated / negligible level | `< 8e²KJ/π*` / `< 2eK/π*` | `< 4Je²M†` / `< eM†` — identical | 3682–3684 |
| 2L: largest sample | `16e²KJ/π*` | `8Je²M†` — identical | 3684–3685 |
| 2L: the count | `2M_j^neg p(s_je^{−x}) ≤ 16e²KJe^x` | `16KJe²·e^x` — identical | 3691 |
| 2L: points near a level | `≤ max(K, 32e²KJe^x)` | `32KJe²e^x + 4K` | 3694 |
| 2L: rounding of `x_{l−1}` into `b + ℕ` | factor `e` | factor `e` | 3703–3704 |
| 2L: cost | `1 + M̄ + Σ_l min{M̄, (J+1)cnt}·C_l` (each rung once per point) | `Σ_{j≤J}Σ_l min(8Je²M†, 32KJe³e^{x_{l−1}}+4K)(l+1)C_l` (an over-count of mine; the `l = 0` term and the reference query are not displayed) | 3707 |
| 2L: width | `1 + 4Je^{b+1} + e^b + e^G` | the same | 3670–3672 |
| 2L⁺: width, four terms | as in the theorem | the same | `K_REPORT` Step 4 |
| 2L⁺: conditions [N], [P] | as above | the same | Step 5 |
| 2L⁺: `M_j^neg ≤ (1+η)e^λν₀M†`, `M ≤ M̄` | the same | the same | Step 6 |
| 2L⁺: the count | `c_η⁻¹e^λ·ν·e^x` | the same (`close_points_bound'` [V] is its algebra) | Step 7 |
| 2L⁺: per-rung calls per level | `min{M_j, cnt(x_{l−1})}` | the same | Step 8 |

I could reproduce every inequality of both proofs; there is no step that I was unable to derive.
The differences are in what is written down, not in what is true: see m1–m4 in §2.7.

### 2.5 The five earlier accountings (D45), and whether the final proof repeats them

1. **Single threshold** (coordinator's brief to workstream H).  *What was wrong:* it counted, for an
   outer point at gap `G` below one threshold `t`, a one-sided inner bound at accuracy `G`; but
   one-sided certificates bound `Σ min(Z_a, t)` only by `Mt` while the main term can be `Kt`, so the
   accuracy needed is relative to the estimate and Markov gives no bound on the number of points at
   small gap.  *Not repeated:* the final algorithm never estimates a mean of bracketed values.  Lower
   and upper end of a level come from the **same** integer `N` (`p̲ = N/((1+η)M)`, `q = N/((1−η)M)`); the
   width never needs `Σ(U_a − L_a)` small.
2. **v1** (workstream H).  *What was wrong:* it counted the points within gap `γ` of a level as
   `e^{n(γ−g₁)}`, i.e. it let the negligibility tolerance reduce the count.  *Not repeated:* the count is
   `ν·e^x` with no factor `e^{−b}` — the `e^b` in `M_j^neg ∝ s_j/(ℓe^b)` cancels against the `e^b` in
   `p(s_i) ≤ e^bℓ/(c_ηs_i)`; and the bound is **attained** up to a constant (my runs reach `0.87` of it,
   §3.2; the engineering division reports `0.95`), so no smaller count can be true.
3. **v2**, 4. **v4** (workstream H).  *What was wrong:* they forgot that the first levels above a bulk
   already put `e^{nβ}` points at the finest inner accuracy.  *Not repeated:* the term is the endpoint
   `γ = β` of the supremum in (11.18.2), `min(β, μ) + (1−φ)T(β/(1−φ))`; in the proof it is the last rung,
   `(J+1)·cnt(x_{L−1})·C_L` with `x_{L−1} ≈ b`.  In my runs on flat bulks all points of the levels just above
   the bulk do go to the last rung (calls per level up to `0.38` of the bound, §3.3).
5. **CLOSE** (coordinator; the tail lemma at every level).  *What was wrong:* not wrong but unproved —
   it needs two-sided inner accuracy on the points that carry each stratum.  *Not repeated:* the upper
   tail lemma enters the returned bracket once, at the closing pass; Algorithm 2L⁺ does use a tail
   lemma at every populated level, but the *lower* one, which needs only the one-sided certified
   fraction `p̲`.

The sixth item of D45 — the closure test at `r = n_o` (a tail lemma applied to the whole cube) — is
absent from both final texts ("no closure at `r = n_o`", `tail := +∞`), and my mutation that restores it
returns an invalid pair in 48 of 48 runs (§3.1).  The necessary condition "no level below the hinted
exponent" is a theorem for the recursion as defined (`exactRec_ge_hint` [V]).

### 2.6 The assembly into exponents: what is proved, what is machine-checked, what depends on `n`

**One level → (11.18.2).**  From the cost of §2.3: the outer sample has exponent
`φθ_na((g−β)/φ)` because `n_o⁻¹ ln Γ̃(ρn_o) → KL(ρ‖p_u)` on `[p_u, ½]` (explicitly
`Γ̃(r) ≤ (m+1)e^{2u}exp(m·KL((r−1)/m‖p_u))`, inequality (3.0) of `K_REPORT.md`; checked on exact tables,
§3.5) and `|B(m,ρm)|/2^m = e^{−m·KL(ρ‖½)+O(log m)}`; the points that need the rung `x_l` number at most
`e^{x_{l−1}}·poly`; an inner call costs `e^{n_iT(ξ_l)+o(n_i)}`.  With `γ = (1−φ)ξ_l` this is the bracket of
(11.18.2) plus the ladder step `η₀`.  **[P; re-derived.]**

**Levels → `θ_hint` (Theorem 11.54).**  Two routes, both re-derived:
(i) *theory report, lines 3800–3818* (left limits): the assembled family has `T′ ≤ min(T, R[T])(·⁻) + η₀`;
the shift `R[T̃](g) ≤ R[T](g−ε) + ε + η′` for `T̃ ≤ T(·⁻) + η′` (replace `β` by `β+ε`, `γ` by `γ−ε`); the
induction `T̃_{k+1} ≤ T_{k+1}(·⁻) + η_k + 2η₀`.  One step is left implicit there: that the infimum over a
*countable dense* set of tuples `(φ, β, g, η₀)` reaches `inf_{g<ξ} R[T](g)`.  It does — for fixed `ζ`
the bracket is continuous in `(φ, β, g)` apart from the constraint `ζ ≥ β/(1−φ)` and the factors
`(1−φ)ζ`, `(1−φ)T(ζ)`, which only decrease when `φ` is increased slightly and `β` is kept with
`β′/(1−φ′) ≥ β/(1−φ)`; so a tuple can be approximated from the good side — but the sentence should be
there (m4).
(ii) *`K_REPORT.md` Proposition E* (no left limits): by induction on `k`, for all `g < g′` and `ζ > 0` a
family with `T_F(g′) ≤ T_k(g) + ζ`; the ladder of step `k+1` is shifted by `ι ≤ g′ − g` so that the inner
families are asked only at rates slightly above their nominal ones.  I checked every inequality
(`(1−φ)ξ_L ≤ β + (1−φ)ι < g′`; `μ′ ≤ μ`; the three contributions `ζ/4`; the case `y_L = u < β/(1−φ)`, where
`T_k(y_l) = 0` because `u > ε*`).  Route (ii) is the cleaner one and is the one Theorem 11.58 uses.

**Bounded accuracy (Theorem 11.58).**  `φ = min(½, η/a)`, `ξ = min(ε*/2, φη)`; a family with extensive
exponent `≤ h + η` at the rate `ξ` (Proposition E(b), from (R)); the base family (`t₀ ≤ a`); then `m`
applications of the two-rung level, `t_{m+1} ≤ max{φa + (1−φ)(h+η), (1−φ)(ξ + t_m)} ≤
max{h + 2η, (1−φ)t_m + φη}`, so `t_m ≤ η + max{h+η, (1−φ)^m a}`.  **[P; re-derived; the last implication
is `two_rung_bound` [V].]**

**Which part is Lean, and what exactly it states** (`lean/R6Axioms.lean`, `lean/R6Axioms2.lean`: statements
printed, compiled with `lake env lean`, exit 0; all depend on `[propext, Classical.choice, Quot.sound]` only):

| declaration | what it states | what it is in the paper |
|---|---|---|
| `admissible`, `Rstep`, `exactRec` (`BoundedAccuracy.lean`) | `R[T](g) = sInf{B : ∃ 0<β<g, 0<φ<1, ∀γ≥β, min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ)) ≤ B}`; `T₁ = θ_na`, `T_{k+1} = min(T_k, R[T_k])` | the recursion (11.18.2), exactly (index shifted by one) |
| `exactRec_reaches_hint` | `0<u → 0<g<ε* → 0<η → ∃k, T_k(g) < θ_hint(g) + η` for `θ_na = cubeNa u`, `θ_hint = cubeHint u` | statement (R) = Theorem 11.53(d) with no hypothesis left |
| `cubeNa_isLeast_allRadii`, `cubeHint` (`CubeHintPair.lean`) | `cubeNa u x = min{KL(ρ‖½) : 0≤ρ≤1, KL(ρ‖p_u) ≤ x}` for `x ≥ 0`; `cubeHint u e = KL((Λ₁+e)/u‖½)` | the Lean functions are the paper's `θ_na`, `θ_hint` |
| `exactRec_ge_hint`, `exactRec_tendsto_hint` | no level below `θ_hint` (clipped at `ε*`); convergence | Theorem 11.53(b) "≥", (d) |
| `two_rung_bound` | the iteration of Theorem 11.58 for an abstract sequence `t` | last line of the proof |
| `certified_lower_sum_le_mean`, `populated_part_le`, `close_points_bound'`, `width_le` | four algebraic inequalities | the algebra of Steps 3, 4, 7 of K1 |
| `cube_exact_dip_randomized` (`QueryRefinements.lean`) | for a finite mixture of consistent deterministic query algorithms that is `(ε/2, δ)`-correct on the class: if the dip of depth `r` moves `ln Z` by more than `ε` and every open ball has `≤ B` points, `(1−2δ)2ⁿ ≤ E[#distinct queries at 0]·B` | Theorem 11.25(a) |
| `cube_nonadaptive_bound` (`NonAdaptive.lean`; `lean/R6Axioms2.lean`) | the same for mixtures whose query set does not depend on the function: if flattening every cone at level `R` lowers `ln Z` by more than `ε` and every open ball `{c·dist < R}` has `≤ B` points, `(1−2δ)2ⁿ ≤ E|Q|·B` | Theorem 11.45(b); the lower bound of Corollary R6.2 (the two finite sums are evaluated numerically there) |

**Is the paper step from the abstract recursion to the algorithm's exponent filled?**  Yes, on paper:
Corollary K1.b + Proposition E (extensive levels) and Theorem K2 (bounded level).  **Not** in Lean:
the algorithm, its events, the tail lemmas and Harper's theorem, the closing radius, the sample
sizes, the count *as a statement about the algorithm*, termination, the cost sum, Lemma 11.55,
Proposition 11.57, the assembly.  The label of Theorem 11.56, "the algebra of the width and of the
count V", is accurate; the status paragraph of §11.18 ("the count of evaluations — the content of
the theorem — is not [machine-checked]") is accurate.

**"Exponent `h`" or "for every `η` exponent `≤ h + η`"?**  The latter.  The proof gives, for every
`η > 0`, a family `G_{m(η)}` — `m ≈ ln(a/h)·a/η` bounded levels on top of `k(ξ, η/2)` extensive levels at
the rate `ξ ≈ η²/a` — with cost `exp(n(h + 2η) + o_η(n))`.  Because Theorem 11.58 is a statement about the
*least* cost at each `n`, this suffices: `limsup n⁻¹ ln(min cost) ≤ h + 2η` for every `η`.  No single
algorithm with exponent `h` is exhibited (a diagonal sequence `η_n → 0` would give one, with an `o(n)`
that nobody has bounded; `k(ξ, η)` comes from a Lean proof that I did not read and the report gives no
rate for it — numerically `(τ_k − h)/a ≈ 0.65/k²` [N, theirs]).  **What depends on `n`:** in Theorem
11.56 nothing is asymptotic; in Proposition 11.57 and Theorems 11.54/11.58 the `o(n)` collects the
polynomial factors (`K, J, ν₀, 1/λ, 1/η², 1/η′, 1/θ` at every level — with accuracies `ε/2^j` down the
`m` levels), the `O(√n_o)` of the outer sample at each bounded level (Lemma 11.55(d); it is real:
`(ln(1/π†) − ma)/√m` reaches `2.9` in R8's tables), and the unquantified `o(n_i)` of every inner
family.  The theory report's own estimate "heuristically not better than `n^{3/4}`" (Remark (2) after
Theorem 11.58) is consistent with what I see and is not a theorem.

### 2.7 Findings

**Critical: none.  Major: none.**

Minor (each with location, what is missing, and the repair; "closed" = I give the missing line):

* **m1 — abort rule of Theorem 11.52 is still the post-hoc one** (`docs/THEORY_REPORT.md` line 3649:
  "If the number of queries exceeds the bound of the cost proof below … stop").  Tested after the
  fact, the cost is bounded by the bound *plus* one inner call.  Referee R8's m1 corrected this for
  Theorem 11.56 (line 3986–3989: "before every inner call"); the text of §11.18 was not changed.
  Repair: the same sentence.  Closed.
* **m2 — the displayed cost of Theorem 11.52** (line 3707) sums over `l` a term containing `x_{l−1}`,
  undefined at `l = 0`, and omits the reference query; read literally with `l ≥ 1` it omits the one
  query per sampled point.  Repair: `1 + (J+1)·8Je²M† + Σ_{j≤J}Σ_{l≥1}…`.  No exponent changes.  Closed.
* **m3 — a case missing in the count of Theorem 11.52** (line 3689: "let `s_i` be the largest level not
  above `s_je^{−x}`"): for `x > j` there is no such level.  Then `p = 1` and
  `2M_j^neg ≤ 4KJe·e^{j−b} < 4KJe·e^{x−b}` because `ℓ ≥ s₀`.  (`K_REPORT.md` Step 7 has this case; R7 §3.7
  mentions it.)  Closed.
* **m4 — the assembly of Theorem 11.54** (lines 3804–3810).  (a) "the cheapest among the old one and the
  first `d` tuples whose accuracy is at most `x`" admits a tuple at a dimension `d` where its procedure
  is not yet a bracket procedure: the failure bound of Theorem 11.52 is proved "for `n ≥ n₀(η₀)`" (line
  3663), and `gd + ln(4eJ+3)` (line 3805) is its accuracy only when `b ≤ G`, i.e. for
  `d ≥ β/((1−φ)(g−β))` (otherwise `b + ln(4eJ+3)`).  Repair: admit a tuple from its own `n₀` on.  (b) the
  passage from a countable dense set of tuples to the infimum needs the one-sided approximation
  described in §2.6.  Both are routine; the route through Proposition E (`K_REPORT.md` §3.3), where
  `θ` is chosen so that the accuracy is exactly `Gn` and Theorem K1 has no `n₀`, avoids them.  Closed.
* **m5 — "likewise in expectation" and the model of the lower bound** (line 4056).  True, and worth one
  sentence in the text: the machine-checked lower bound counts *distinct* evaluated points of a finite
  mixture of deterministic algorithms at the zero function; the upper bound counts evaluations with
  multiplicity in every run.  The two conventions are compatible in the direction needed.  No gap.
* **m6 — detection of the Harper term in harnesses.**  Not an error of the text: in my runs the
  mutation "no Harper term" is detected in 1 of 47 runs only (R8: 2–15 %), i.e. most instances never
  exercise the one step that distinguishes Theorem 11.56 from Theorem 11.52 at a bounded accuracy
  (a populated level whose closing radius is just above `r†`).  A harness that reports "no violation"
  should report how many populated passes had `min{Γ̃/c_η, Γ″} ≤ θ` decided by `Γ″`.  (My own records
  do not: in the valid 2L⁺ campaigns 315 of 2424 closures happen at a populated pass, and I did
  not log which of the two terms decided them.)
* **m7 — the cap remark of `40c5bd7` has one uncovered pass** — see §2.8.  Closed.

### 2.8 The remark "the sample-size cap can be lowered" (commit `40c5bd7`) — proved, with one pass added

*Statement* (theory report at `40c5bd7`, remark after Theorem 11.56; `[P]`, theirs, unrefereed).
`Δ := ⌈λ/u⌉`, `π‡ := 2^{−n_o}|B(n_o, r†−Δ)|`, `M‡ := K/((1−η)π‡)` (`M‡ := K2^{n_o}/(1−η)` if `r† < Δ`).  **In every
run every sample is `K` or has fewer than `2max{e^λM†, M‡}` points.**  For Theorem 11.52: `M < 2e·M†`.

*My derivation* **[P; checked on every run of §3: the cap was never reached, largest observed ratio
in §3.2].**  Level 0 is populated at `M = K` in every run: the rung-0 bracket of any point has
`L = e^{−ψ(a,0)−un_i} ≥ e^{−ψ₀−un_o−un_i} = s₀ > s₀e^{−b}`, so every point is high without an inner call.  A
later level `j` follows a level that was left.  (1) After a negligible level, `M_j^neg ≤ e^λM_{j−1}^neg ≤
e^λM_{j−1} < e^λM†`, so every sample of level `j` is `< 2e^λM†`.  (2) After a populated level, `q_{j−1} > π†`
gives `p̲_{j−1} > c_ηπ†` and a Harper radius `≥ κ(r†+1)`, so `ℓ ≥ s_{j−1}e^{−b}max{c_ηπ†, 2^{−n_o}T(κ(r†+1))}`.
Let a pass of level `j` be unpopulated with `M ≥ M‡`.  If `r† ≥ Δ`: `q ≤ π‡`, so `r ≤ r† − Δ`; termwise
`E_{r−1} ≤ e^{−u}E_r`, hence `tail = s_j2^{−n_o}E_r ≤ s_{j−1}e^{λ−uΔ}2^{−n_o}E_{r†} ≤ s_{j−1}2^{−n_o}E_{r†}`, and [P] at `r†`
(either `E_{r†} ≤ θT(κ(r†))` or `E_{r†} ≤ c_ηθ·max(1, |B(r†−1)|) ≤ c_ηθ2^{n_o}π†`) gives `tail ≤ θe^bℓ`: the run
stops.  All of this agrees with the published proof.

*The uncovered pass.*  For `r† < Δ` the published proof says only "(a pass with `2^{n_o}q < 1` has an
empty tail)".  But `M = M‡ = K2^{n_o}/(1−η)` can lie in the doubling sequence (`η = ½`), and then
`2^{n_o}q = 1` exactly: `r = 0` and `tail = s_j2^{−n_o}E_0 ≠ 0`.  If that pass did not close and had
`M < M_j^neg`, the next sample would have exactly `2M‡` points — not "fewer than".  It does close:
* if `r† ≥ 1`: `E_1 = (e^{2u}−1) + m(e^u−1) ≥ (m+2)(e^u−1) = (m+2)E_0`, so with `λ ≤ 1`,
  `e^λE_0 ≤ (e/3)E_1 < E_{r†}`, and `tail ≤ s_{j−1}e^λ2^{−n_o}E_0 < s_{j−1}2^{−n_o}E_{r†} ≤ θe^bℓ` as before;
* if `r† ∈ {0, −1}`: `M† ≥ M‡`, so the cap is `2e^λM† > 2M‡`, and no sample exceeds `2M‡` because a pass
  with `M > M‡` has an empty tail.
So the statement is true as published, *given* `λ ≤ 1` (a hypothesis of Theorem 11.56 that erratum m3
of `K_REPORT.md` calls unused — here it is used), and its proof needs these three lines.  The 2L form
`M < 2e·M†` I re-derived directly: an unpopulated pass with `M ≥ max{M†, M_j^neg/(4Je)}` has
`q ≤ π*`, `Γ̃(r) ≤ e^{G−b}/4`, `tail ≤ s_j(2K/M)e^{G−b}/4 ≤ e^Gℓ`, and `M_j^neg ≤ 4Je²M†`.  **Verdict: proved
with a gap that I close (minor).**  Effect on the cost: the first branch of every minimum in `C_max`
loses a factor of order `ν₀`; in my tables `ln C_max` drops by between `0.1` and `11` (§2.9), no exponent changes.

### 2.9 An every-`n` statement (no `o(n)`), and a certified finite-`n` separation

The brief asks whether the cost can be stated and proved with explicit constants for every `n` on a
sub-class.  **It can, and on the whole class** — for two levels.  The `o(n)` of §§11.18–11.19 enters
only (a) when binomial sums are replaced by exponents and (b) through the unquantified `o(d)` of an
inner *family*; with the base bracket as inner procedure neither is needed.

**Theorem R6.1 (two levels, every `n`, the whole class) [P: the composition of Theorem 11.56 = K1 and
Proposition 11.57(a) = K0, both re-derived here; every constant computed by my own code and equal, to
all published digits, to the engineering division's (§3.3)].**  Let `u > 0`, `n ≥ 2`, `1 ≤ n_o ≤ n−1`,
`n_i = n − n_o`, `0 < λ ≤ 1`, `0 < η ≤ ½`, `η′ > 0`, `θ > 0`, `ν₁ ≥ 1`, `b > 0`, `0 < δ < 1`, and a ladder
`2un_i = x₀ > x₁ > … > x_L`, `x_L ≤ b`.  Let `J, ν₀, r†, π†, m_max, K, ν, M†, M̄, δ′, cnt` be the constants of
§2.1.  For `l = 1, …, L` let `η_l = min(½, tanh(x_l/4))`, `K_l = ⌈3(1+η_l)η_l⁻² ln(4/δ′)⌉`, `r*_l` the largest
radius `≤ n_i − 1` with `ln(1 + Γ″_{n_i}(r′)) ≤ x_l − ln((1+η_l)/(1−η_l))` for all `r′ ≤ r*_l` (`Γ″` with `η_l`),
`M_l = ⌈K_l2^{n_i}/((1−η_l)|B(n_i, r*_l)|)⌉`, and `C_l = min{2M_l, 2^{n_i}}` (`2^{n_i}` if no radius qualifies).
Then, for **every** `ψ ∈ L_u(Q_n)`, Algorithm 2L⁺ with the two-sample bracket of accuracy `x_l` on the
fibres (enumeration where `C_l = 2^{n_i}`):

* makes at most `C_max = 1 + 2M̄ + Σ_{l=1}^{L} min{2M̄, (J+1)cnt(x_{l−1})}·C_l` evaluations **in every run**;
* returns, with probability at least `1 − δ`, a pair `L ≤ A ≤ U` with
  `U/L ≤ e^{x_out}`, `x_out = ln[(2p_u)^n + e^b(e^λ(1+η)/(1−η) + η′ + θ)]`.

`C_max` and `x_out` are finite expressions in binomial coefficients of `n_o`, `n_i` and in `e^u`; there
is no `o(n)` and no "for `n` large".  With the cap of §2.8, `M̄` may be replaced by
`2max{e^λM†, M‡}` in `C_max` (my tables give both values; the second keeps `m_max`, `K`, `δ′` unchanged).

*Proof.*  Proposition K0 makes `I_l` a bracket procedure for `(n_i, x_l, δ′)` with cost `2M_l` (two
samples; §0: re-derived — the three events, `t⁺`, `t⁻`, the two tail lemmas, `r̂ ≤ r*_l ≤ n_i − 1`);
enumeration is exact.  Theorem K1 (§2.3–2.4) then applies verbatim.  ∎

*A closed form for the dominant factor* (Lemma 11.55(d), checked on exact tables `m ≤ 4000`, §3.5): if
`θ ≤ 2e^{u(m₀+2)}`, `ν₁ ≥ 2e^un_o/θ` and `r₊ := ⌊p_un_o − √((n_o/2)ln(2e^{u(m₀+2)}/θ))⌋ ≥ p_un_o/2`, with
`m₀ = ⌈u⁻¹ln((1+η)/(1−η))⌉`, then

    ln M̄ ≤ n_o·a + (u + ln 4)(1 + √((n_o/2)·ln(2e^{u(m₀+2)}/θ))) + ln(n_o+1) + ln(2(1+η)e^λν₀K/(1−η)) ,

and the same form with `d = n_i`, `e^{x/2} − 1` for `θ` holds for the base bracket at a bounded accuracy
`x`.  With (3.0) for the extensive rungs this gives a two-level bound of the form
`exp(n·max{…} + c₁√n + c₂ ln n + c₃)` whose constants are explicit in principle; I did not write them out —
the tables below are computed from the exact `C_max`, not from such a closed form.

**Where it resists.**  For `k ≥ 3` levels the bound is still an explicit finite recursion in `n`
(Theorem K1 applied to itself), but no closed form with an explicit `o(n)` follows from the proofs:
the number of levels needed for a given `η` comes from the convergence of the recursion, for which
the Lean proof gives existence and the reports give numerics only; each bounded level loses a factor
`e^{O(√n)}`; and the inner accuracies shrink like `ε/2^j`.  An explicit statement
"`min_alg cost ≤ exp(nh + C·n^α)` for all `n ≥ n₀`" with `α < 1` is **not** proved by anyone, and I could not
prove one in the time I had: the missing input is a rate for `T_k → θ_hint`.

**Corollary R6.2 (a certified separation at explicit finite `n`) [P given Theorem R6.1 and Theorem
11.45(b) — the non-adaptive lower bound, machine-checked up to two finite sums; numbers from exact
binomial tables with 40-digit arithmetic, `everyn.py`, `separation.py`].**  Take the design of
`K_REPORT.md` §6.4: `b = 0.5`, `λ = 0.2`, `η = η′ = θ = 1/20`, `ν₁ = 2e^un_o/θ`, `δ = 0.05`, inner rates
`ε*·0.85^i` (`i < 40`), `n_o = ⌊n/2⌋`; certified accuracy `x_out = 0.872`.  Let `LB_na` be the lower bound
of Theorem 11.45(b) at the same accuracy and `δ`: `(1 − 2δ)2ⁿ/|B(n, R−1)|` with `R` the least radius such
that flattening a cone below `R` lowers `ln Z` by more than `x_out`.  Then (natural logarithms of
numbers of evaluations):

| `u` | `n` | `ln C_max` (adaptive, every run, every instance) | `ln LB_na` (every non-adaptive algorithm, in expectation, on some instance) | `ln` of the plain two-sample bracket | `ln` of the hinted lower bound |
|---|---|---|---|---|---|
| 1 | 1000 | 126.3 | 110.9 | 149.7 | 31.7 |
| 1 | 1350 | 150.8 | 149.0 | 193.9 | 42.0 |
| 1 | **1400** | **154.0** | **155.0** | 199.9 | 43.5 |
| 1 | 2000 | 193.1 | 221.1 | 273.0 | 61.1 |
| 1 | 4000 | 320.8 | 441.3 | 511.1 | 120.1 |
| 1 | 8000 | 566.9 | 883.1 | 976.9 | 236.8 |
| 1 | 16000 | 1045.1 | 1767.6 | 1897.4 | 470.3 |
| 2 | 520 | 170.1 | 169.1 | 228.8 | 53.4 |
| 2 | **540** | **173.9** | **176.5** | 236.2 | 55.1 |
| 2 | 1000 | 264.1 | 327.2 | 402.7 | 100.4 |
| 2 | 4000 | 814.3 | 1306.6 | 1448.0 | 393.2 |
| ½ | 4500 | 136.3 | 135.7 | 166.8 | 37.3 |
| ½ | **4700** | **139.6** | **141.5** | 173.7 | 39.0 |
| ½ | 8000 | 197.4 | 240.7 | 279.9 | 64.5 |
| ½ | 11000 | 249.3 | 331.1 | 375.8 | 87.5 |

So, for instance, **at `n = 2000`, `u = 1`, bracket ratio `e^{0.872}`, `δ = 0.05`: every non-adaptive
algorithm needs more than `e^{221}` evaluations in expectation on some member of `L_u(Q_n)`, while
Algorithm 2L⁺ needs at most `e^{193.1}` in every run on every member** — a factor `e^{28}`, with every
constant explicit.  On the grids I computed (`u = 1`: 17 sizes from `250` to `16 000`; `u = 2`: 12 sizes
from `250` to `4000`; `u = ½`: 11 sizes from `1000` to `11 000`; outer fractions `0.35–0.60`, `0.45–0.55` at the
refinement sizes, `0.50` only at `n = 16 000`), the certified bound falls below the non-adaptive lower
bound at `n = 1400` (`u = 1`; at `1380` the two agree to the first decimal of the logarithm), `540` (`u = 2`),
`4700` (`u = ½`) and stays below at every larger size computed.  What this does **not** say: it is a statement at the listed `n` (monotonicity in `n` is
observed, not proved); the numbers are far beyond anything executable; and it compares a paper-proved
upper bound with a lower bound whose closed forms are paper calculus.  What it adds to the reports:
they compare the algorithm with the *plain bracket* (an upper bound for non-adaptive algorithms,
crossover `n ≈ 500` at `u = 1` in ENG-RES-0008); the comparison that makes "adaptivity helps" a theorem
at a given `n` is with the non-adaptive *lower* bound, and that crossover is at `n = 1400`.  Note that
`ln LB_na/(na)` is between `0.99` and `1.02` at every size: at a bounded accuracy the non-adaptive lower
bound is essentially `e^{na}` already at `n = 250`.

**On the zero residual** the run with real base brackets is deterministic and its cost is an exact,
explicit function of `n`; my engine reproduces the published values (§3.3).  The zero residual is the
*cheap* instance for this algorithm (it closes at a radius far above `r†`), so an every-`n` statement
restricted to it would be weaker than Theorem R6.1 in the only direction that matters.

## 3. Numerics

Everything in this section is **[N]** — independent *replication* with my own code
(`experiments/science/ws_R6/`); no script of the authors, of their referees or of the engineering
division was run or read.  Python 3.13, numpy 2.5.3, mpmath 1.3.0,
at most two processes, every job under ten minutes.  The machine was shared and heavily loaded
(load average 10–15 on 4 cores), so several campaigns were cut by their time limit: the numbers
below are the runs that completed, and every number in the tables is produced from the data files by
`make_section3.py` (`data/summary_all.json`), not transcribed.

### 3.1 The implementation and its checker

* `r6lib.py` — exact tables on the outer cube (`|B|` as integers; `E_r`, `T_m` with 40 digits); the
  constants of Theorem 11.56 (`Params2LP`) and of Theorem 11.52 (`Params2L`); the two algorithms, pass by
  pass (`Run`).  `q`, `p̲`, the closing radius and the Harper radius are exact (Fractions against
  integer ball sizes: `q = 1` gives `r = n_o` exactly); levels, `ℓ`, `Σ`, tails are 40-digit numbers;
  brackets are float64 logarithms.  The outer sample is literal: the list `a₁, a₂, …` is drawn at
  random, block by block of the doubling sequence, as exact counts of the classes of outer points with
  equal fibre average (sequential binomials; chunks of `2^61` so that blocks of up to `2^83` points
  can be drawn — `big_binomial`, tested against means and variances), one bracket per (block, class),
  or one unit per point for explicit cubes.
* `checks.py` — after every run, every claim of the theorem against quantities the algorithm never
  sees (the exact tail `p(t)` and mean `A` of the instance): *for every run* — closing radius of every
  level left (iii), `M ≤ max(K, 2M_j^neg)`, `M_j^neg ≤ (1+η)e^λν₀M†`, `M ≤ M̄` (iv), the cap of `40c5bd7`,
  the width of a pair returned through the test, queries `≤ C_max`; *on the good event* — evaluated
  as "(V1), (V2), (V3) hold at every pass the run actually made", a superset of the proof's event —
  no abort (i), `L ≤ A ≤ U`, `p(s_j) ≤ q` and `p̲ ≤ p(s_je^{−b})` at every pass, `ℓ ≤ A` at every update
  (ii), the count inequality and the sampled count against `cnt` (v), calls per level and rung and the
  total against claim (vi).  For Algorithm 2L: the corresponding statements of Theorem 11.52 (`r > r†`,
  `M ≤ 8Je²M†`, `M < 2eM†`, width, the count `32KJe²e^x + 4K`, calls per level, the cost display
  completed as in m2).
* `instances.py`, `campaign.py` — product instances `ψ(a,b) = −F(d(a,c)) + s_in|b|`: outer radial
  profile `F` with increments in `[−u, u]` (17 families: flat, cones of slope `u, u/2, u/4`, dips —
  also at the radius `r†`, at `Λ₁n_o/u` and at `p_un_o` —, flattened cones, plateau-then-cone, the
  equal-mass staircase `W ∝ 1/|B(d)|`, four kinds of random walk, the 2-periodic profile, staircases,
  profiles on the level grid, two plateaus), reference point in the shell `0`, `n_o/2`, `n_o` or random,
  inner slope `s_in ∈ {0, ±u, ±u/2}` (it moves the reference value inside the trivial bracket).
  Inner behaviours: a valid bracket of ratio `e^{x_l}` placed with `W` at the middle / top / bottom, at
  random, narrower than promised, exact, or by one of two adversaries that keep a point unclassified
  at the current level whenever a valid bracket allows it and then make it high, resp. low; mixtures
  within a run.  *Invalid* behaviours, to test the every-run statements: a bracket entirely above or
  below `W`, one `2.5` times too wide, the rung-0 bracket again, and "LAZY" (the rung-0 bracket at
  every rung but the last, a valid bracket at the last).

*Negative controls* (`data/MUT_*_7.jsonl`, 48 runs each, six cells): each of the five mutations of
`K_REPORT.md` is detected by the check it should break.

| mutation | detected as | runs in which it is detected |
|---|---|---|
| negligibility threshold without `e^{−b}` | the count inequality (v) | 24 of 47 (and `M_j^neg` above its bound in 8) |
| no Harper term | a level left with `q ≤ π†` (iii) | 1 of 47 |
| lower end without the sum `Σ` | width | 26 of 47 |
| tail lemma at `r = n_o` | the returned pair has `L > U` | 48 of 48 |
| `q` without `1/(1−η)` | certificate `p(s_j) ≤ q` false | 26 of 48 (one invalid final bracket) |

### 3.2 Literal runs with a simulated inner oracle (`campaign.py`; data `data/<campaign>_<seed>.jsonl`)

| campaign | algorithm | `K` | cells | inner behaviour | runs completed (discarded) | closed / `L>U` / aborted | levels left populated / negligible | good event failed | **violations: every-run claims / good-event claims** | invalid final bracket (of these on the good event) |
|---|---|---|---|---|---|---|---|---|---|---|
| `A_small` | 2L⁺ | theorem | 8 cells, `n_o ∈ {10,…,40}`: Theorem-K2 parameters at `x ∈ {1, 2, 4}`, two general cells, one Corollary-K1.b cell | valid (10 behaviours) | 1664 (0) | 1664 / 0 / 0 | 340984 / 180 | 0 | **0 / 0** | 0 (0) |
| `A_ties` | 2L⁺ | theorem | 5 cells, `n_o ∈ {24, 32, 100, 120}`, dyadic `λ`, `un/λ ∈ ℕ`, flat fibres, profiles on the level grid | valid (ends of brackets exactly at `W`) | 451 (49) | 451 / 0 / 0 | 159838 / 1819 | 0 | **0 / 0** | 0 (0) |
| `A_medium` | 2L⁺ | theorem | 12 cells, `n_o ∈ {60,…,1000}`, `u ∈ {½, 1, 2, 3}`: eight bounded-regime cells and four Corollary-K1.b (extensive) cells (12 of the runs are on three earlier extensive cells whose outer sample is trivial) | valid (10 behaviours) | 309 (11) | 309 / 0 / 0 | 339785 / 1517 | 0 | **0 / 0** | 0 (0) |
| `D_2L` | 2L (Thm 11.52) | theorem (`K = ⌈24 ln(2^{n+6}n³/δ)⌉`) | 8 cells, `n ∈ {40,…,3000}`, `n_o ∈ {12,…,1500}` | valid (10 behaviours) | 137 (0) | 137 / 0 / 0 | 143031 / 298 | 0 | **0 / 0** | 0 (0) |
| `B_reducedK` | 2L⁺ | `K ∈ {8, 20, 50}` | 5 cells, `n_o ∈ {40,…,400}` | valid | 201 (1) | 201 / 0 / 0 | 138210 / 1443 | 51 | **0 / 0** | 0 (0) |
| `B_invalid` | 2L⁺ | theorem (one cell `K = 20`) | 7 cells, `n_o ∈ {12,…,400}` | **invalid** (above `W`, below `W`, too wide, trivial, mixtures) | 395 (5) | 195 / 21 / 179 | 213534 / 8066 | 395 | **0 / 0** | 159 (0) |
| `B_lazy` | 2L⁺ | theorem | 6 cells, `n_o ∈ {40,…,400}` | **invalid** (LAZY: every refined point reaches the last rung) | 319 (1) | 170 / 0 / 149 | 234570 / 1690 | 319 | **0 / 0** | 0 (0) |
| `D_2L_off` | 2L (Thm 11.52) | theorem and `K ∈ {10, 30}` | 5 cells, `n ∈ {60, 600, 1200}` | valid and **invalid** | 210 (0) | 183 / 0 / 27 | 213063 / 357 | 99 | **0 / 0** | 30 (0) |

Reading.

* **With the constants of the theorems and valid inner answers** (2424 runs of Algorithm 2L⁺, 137 of
  Algorithm 2L; 60 further runs of 2L⁺ were discarded because a block would have exceeded `2^83` points): every run
  closed; the events of the proof held at every pass of every run; no claim was violated; every final bracket
  contains `A`.  Branches exercised in the 2L⁺ runs: 840607 levels left as populated and 3516 as negligible;
  closures at a populated pass 315, at an unpopulated one 2109 (366 with an empty tail,
  715 at a radius `≤ r†`); largest sample `e^{57.8}` points.  In the 2L runs: 143031
  populated and 298 negligible levels, largest sample `e^{50.9}`.
* **How close the bounds come** (valid runs, 2L⁺): the count inequality `M_j^neg p(s_je^{−x}) ≤ c_η⁻¹e^λνe^x` reaches
  `0.869` of its right-hand side; the sampled count `0.299` of `cnt(x)`; the calls per level and
  rung `0.288` of `min{M̄, cnt}`; the largest sample is `2.07·M†`, i.e. `0.843` of the cap of
  `40c5bd7` and `0.0015` of `M̄`; `ln(queries)/ln(C_max) ≤ 0.843`.  For 2L: largest sample
  `3.03·M†` (`0.556` of `2eM†`), sampled count `0.0849` of `32KJe²e^x + 4K`,
  `2M_j^neg p(s_je^{−x})` at most `0.184` of `16KJe²e^x`.
  The count is the tight claim, as R7, R8 and the engineering division found; the cap `M̄` is loose by the factor `ν₀`.
* **`K` reduced** (`B_reducedK`: `K` replaced by 8, 20 or 50 — the theorem's values are in the hundreds or thousands): the
  events of the proof failed in
  38 of 70 runs at `K = 8`, 13 of 66 at `K = 20`, 0 of 65 at `K = 50`;
  **on every run on which they hold no claim is violated**; the every-run claims hold in all 201 runs;
  0 final brackets were invalid (0 on a run on which the events hold).
* **Invalid inner answers** (`B_invalid`, `B_lazy`: 714 runs; nobody had tested this — in every earlier harness
  (V1) holds by construction).  The statements that Theorem 11.56 makes "for every run, on or off the
  good event" — closing radius above `r†` at every level left, `M ≤ max(K, 2M_j^neg)`, `M_j^neg ≤ (1+η)e^λν₀M†`,
  `M ≤ M̄`, the cap of `40c5bd7`, the width of every pair returned through the closure test, queries
  `≤ C_max` — **held in all 714 runs**.  As allowed off the good event, 159 final brackets were
  invalid, 21 returned pairs had `L > U` (erratum m1 of `K_REPORT.md`: return the trivial bracket), and
  179 runs aborted with a point unclassified at the last rung.
* **The abort rule is not decorative.**  With the behaviour LAZY and rung costs `10^l` (59 runs) no run
  needs it (0 aborts; queries at most `0.021` of the bound of claim (vi)); with rung costs
  `e^{80l}` — the regime of the theorems, where the last rung dominates — **149 of 260 runs stop on the
  query budget**: without the rule their cost would exceed `C_max`.  With the test made *before* the inner
  call the number of queries is `≤ C_max` in every run (runs above `C_max`: 0; largest
  `ln(queries) − ln(C_max) = −0.0003`).  This is the first execution of the branch that
  makes "the cost bound holds always" true (R7's M1).
* **Algorithm 2L off the good event** (`D_2L_off`, 210 runs with reduced `K` and/or invalid answers): the
  every-run statements of Theorem 11.52 (`r > r†` at every level left, `M ≤ 8Je²M†`, `M < 2eM†`, the width,
  the completed cost display) held in all runs; 30 final brackets were invalid, 0 of them on a
  run on which the events hold; 0 violations of a good-event claim on such runs.
* **The cap remark of `40c5bd7` in its degenerate branch** (`capcorner.py`, 4500 runs, `n_o ∈ 3..12`, `λ = 1 > u`,
  `η = ½`): the cap was never reached (largest sample `0.50` of it); for `r† ≥ 1` all
  193 unpopulated passes with `M = M‡` exactly closed; for `r† ∈ {0, −1}` that pass failed to
  close 1255 times and the sample reached exactly `2M‡` in 1133 runs (§2.8).

In total: **3686 literal runs in the campaigns of the table, 0 violations of an every-run claim, 0
violations of a good-event claim on a run where the events hold.**


### 3.3 Reproduction of published numbers (which I had not seen when the code was written)

*The constants.*  `everyn.py` evaluates `C_max` of Theorem 11.56 with the base brackets of Proposition
11.57(a) inside, the plain base bracket, and the hinted lower bound, for the design of `K_REPORT.md`
§6.4.  Entries `ln(·)/(na)`; the second number in each cell is the value in the tables of
ENG-RES-0008 ("cap `C_max` at that `φ`", "plain bracket", "hinted lower bound"):

| `u`, `n`, `φ` | `C_max` | plain bracket | hinted lower bound |
|---|---|---|---|
| 1, 1000, 0.55 | 1.1720 / 1.172 | 1.3493 / 1.349 | 0.2857 / 0.286 |
| 1, 2000, 0.50 | 0.8700 / 0.870 | 1.2303 / 1.230 | 0.2754 / 0.275 |
| 1, 4000, 0.50 | 0.7228 / 0.723 | 1.1516 / 1.152 | 0.2707 / 0.271 |
| 1, 16000, 0.50 | 0.5887 / 0.589 | 1.0689 / 1.069 | 0.2649 / 0.265 |
| 2, 1000, 0.50 | 0.8056 / 0.806 | 1.2285 / 1.229 | 0.3061 / 0.306 |
| 2, 4000, 0.50 | 0.6210 / 0.621 | 1.1043 / 1.104 | 0.2999 / 0.300 |
| ½, 4000, 0.50 | 1.0482 / 1.048 | 1.2440 / 1.244 | 0.2751 / 0.275 |
| ½, 8000, 0.50 | 0.8142 / 0.814 | 1.1546 / 1.155 | 0.2661 / 0.266 |

Three independent implementations (workstream K, the engineering division, this one) therefore agree
on every constant of Theorem 11.56 and of Proposition 11.57(a).  The two lower bounds of §2.9 (hinted and
non-adaptive) were in addition recomputed directly from the definitions of `Δ_k` and `D_R` with a different
arithmetic (float64 logarithms, `crosscheck_lb.py`): in all 184 cells of the separation tables `k*` and `R`
are identical and the logarithms of the bounds differ by at most `1.2·10⁻¹¹`.

*A whole trajectory.*  `flat_exact.py` runs my literal engine, unchanged, on the flat instance with the
inner behaviour "bottom" and the costs of the base brackets:

| `u`, `n`, `φ` | `ln(cost)/(na)` | `ln M/(n_oa)` | closing radius (`r†`) | levels left populated / negligible | ENG-RES-0008 |
|---|---|---|---|---|---|
| 1, 1000, 0.80 | 0.7013 | 0.756 | 255 (180) | 5003 / 223 | 0.701, 0.756, 255 (180), 5003 / 223 |
| 1, 1000, 0.55 | 0.9788 | 0.781 | 179 (119) | 5003 / 128 | 0.979 |
| 1, 4000, 0.50 | 0.6872 | 0.793 | 603 (482) | 20003 / 762 | 0.687 |

(Other cells were stopped to free the machine.)  This is an end-to-end agreement of the pass-by-pass
logic and of the cost accounting with an implementation I have not read.

*The exponents.*  `tau2.py`: `τ₂/a = 0.5001, 0.5004, 0.5056` for `u = ½, 1, 2` (reports: `0.5001`,
`0.5004–0.5006`, `0.5056–0.5057`); the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` to `4·10⁻¹²` on 2001
accuracies; Proposition 11.57(c) on 999 values of `φ`: the bracket with `T = θ_hint` exceeds `h` by at
least `7.6·10⁻⁶` (never below).

### 3.4 Real inner brackets: two levels and three levels (`e2e.py`, `three.py`)

*Two levels.*  Explicit `u`-Lipschitz functions on `Q_{n_o} × Q_{n_i}`, `(n_o, n_i) ∈ {(6,6), (7,6), (6,7), (7,5), (8,5), (5,7)}`
(five random constructions: lower and upper McShane envelopes of random data, additive functions, radial
walks, inf-convolutions of noise), `u ∈ {½, 1, 2}`; every outer point is individual; the inner procedure of every rung is the two-sample
bracket of Proposition 11.57(a) on the fibre with fresh randomness (two samples drawn as exact
multinomial counts over the fibre) and the constants of the proposition for `δ′ = δ/(4LM̄)`; all constants
of Theorem 11.56 from the formulas; `L ∈ {1, 2, 3}`.
**129 runs, 9,786,461 real inner brackets** (224 of 270 rungs by a two-sample bracket,
the rest by enumeration): 0 inner brackets invalid or wider than promised; 0 final brackets
invalid; 0 wider than `x_out`; 0 aborts; violations of every-run / good-event claims:
0 / 0; queries at most `0.006·C_max`.
With `K` (outer and inner) divided by 16 — off the theorems, an attempt to provoke real failures of (V1): 400 runs,
1,844,727 real brackets, 0 of them invalid or too wide (in 0 runs); the events of
the proof failed in 31 runs; 0 invalid final brackets, 0 of them on a run where the
events hold; violations of every-run / good-event claims: 0 / 0.

*Three levels.*  `Q_n = Q_{n_o} × (Q_{n_o′} × Q_{n_i′})`, `(n_o, n_o′, n_i′) ∈ {(3,3,3), (3,3,4), (3,4,3), (4,3,3)}`, `u ∈ {½, 1}`:
outer Algorithm 2L⁺; on every fibre a middle Algorithm 2L⁺ whose *certified* accuracy is at most the
outer rung's and whose failure probability is the outer `δ′`; at the bottom two-sample brackets;
all constants from the theorems; the declared cost of a middle call is the middle `C_max`.  (For run
time an outer point draws its bracket from a pool of independent middle runs on its fibre, as in
R8.)  **19 outer runs, 1152 middle runs, 80,363,188 real bottom brackets** (in 12 of the
outer runs the bottom rung is a two-sample bracket, in the others no radius qualifies and the fibre is enumerated):
invalid or too wide brackets: 0 at the bottom, 0 (invalid) and 0 (too wide) in the middle, 0 and 0 at
the top; violations of an every-run or a good-event claim of Theorem 11.56: 0 and 0 at the middle level,
0 and 0 at the outer level; the outer number of queries stays a factor `e^{5.4}` below its `C_max`.

*What these runs are worth.*  The cubes have 12–13 (two levels) and 9–10 (three levels) coordinates;
at these sizes an inner bracket costs more than enumerating its fibre, and the runs test the logic of
the nesting and the interface "bracket procedure" with real, independent randomness — not the cost.


### 3.5 The inputs, by brute force

`check_tail_lemmas.py`, `check_K4cd.py` (`logs/check_tail_lemmas.log`):

* Harper's theorem in the form used (`|S| ≥ |B(m,k)| ⇒ |N(S)| ≥ |B(m,k+1)|`): all 65 808 nonempty subsets of
  `Q_1, …, Q_4`; 60 000 random and structured subsets of `Q_5, Q_6, Q_7`: no violation.
* Lemma K.1 = 11.43(b),(c) at every threshold of 960 random `u`-Lipschitz functions on `Q_4 … Q_10`
  (McShane extensions, additive, radial walks, inf-convolutions of noise): 34 873 thresholds for (a),
  35 833 for (b), no violation, equality attained (largest ratio `1.000000`).
* Lemma 11.55 = K.4: (a), (b) and inequality (3.0) in 22 583 cases (`m ≤ 2000`, `u ∈ {½, 1, 2}`, four values
  of `η`): largest ratios `0.886`, `0.854`, `0.264`; (c) in 401 cases (`m ≤ 4000`): `min(r† − r₊) = 2`; (d)
  in 290 cases: `max(lhs − rhs) = −7.6`; the binomial median `P(Bin(m, p_u) ≥ ⌊mp_u⌋) ≥ ½` in 27 cases
  (`m ≤ 4000`): smallest value `0.508`.
* Lean: `lean/R6Axioms.lean`, `lean/R6Axioms2.lean` (§2.6).

### 3.6 Adversarial search (`adversarial.py`)

Hill climbing with restarts over the radial profile (one increment in `[−u, u]` per shell), the position
of the reference point, the inner offset and the inner behaviour, with literal runs, one objective at a
time; every run is also checked for every claim.

| cell | objective (a ratio that the theorem bounds by 1) | literal runs | largest value found | violations |
|---|---|---|---|---|
| `n = 80`, `n_o = 40`, `u = 1`, `λ = 0.333` | count inequality (v) | 23 | 0.571 | 0 |
| `n = 48`, `n_o = 24`, `u = 0.5`, `λ = 0.5` | sample / cap of `40c5bd7` | 594 | 0.181 | 0 |
| `n = 200`, `n_o = 100`, `u = 2`, `λ = 1` | count inequality (v) | 74 | 0.461 | 0 |
| `n = 200`, `n_o = 100`, `u = 2`, `λ = 1` | sample / cap of `40c5bd7` | 67 | 0.000 | 0 |
| `n = 160`, `n_o = 80`, `u = 2`, `λ = 0.5` | calls per level / bound (vi) | 58 | 0.144 | 0 |

(In the fourth row no run with a sample above `K` completed: samples near `M†` exceed my sampler in that
cell, so the row is uninformative.)  816 runs, 0 violations.  With these budgets (about 200 s per search on a loaded machine) the hill
climbing does **not** get closer to any bound than the structured instances of the campaigns do (count
inequality `0.869`, sample `0.843` of the cap there); it is a weak search and I report it as such.
A structured sweep aimed at the cap (`capsearch.py`: the cell of the theory division's own example,
`n_o = 24`, `u = λ = ½`, and neighbours; landscapes "plateau, then cone" with every plateau radius, cones,
"cone, then flat"; 1609 literal runs, 0 violations) reaches a sample of `2.46·M†` where the cap is
`4.06·M†` and `M̄ = 847·M†`: `0.61` of the cap (samples move in factors of two, so the
next step would exceed it).  For comparison: the engineering division's search in expectation reports
`0.95` for the count and `1.8·M†` for the sample; K's runs report samples up to `4.5·M†`; the theory division's
harness `3.7·M†` (91 % of the cap) at the same `n_o`, `u`, `λ` (its other parameters are not stated).

### 3.7 Overlap with ENG-RES-0008

Read after my implementation was written; their code was neither run nor read.  *Same:* the algorithm
(K_REPORT §2.2 with errata m1, m10), radial product instances with a reference shell and one inner
offset, the inner behaviours "bottom", "top", "random", the reduced-`K` experiment, the checks (iii)–(vi).
*Their side only:* expectation-level ("mean") runs with a search over instances at `n` up to `128 000`
(7 095 840 runs) and the worst-instance cost tables; 585 000 literal runs at three sizes
(`(u, n_o) ∈ {(½, 300), (1, 120), (2, 48)}`) with one design.  *My side only:* invalid inner answers and the
abort rule; Algorithm 2L of Theorem 11.52 and the extensive regime (their "not started"); ties on the
level grid; the cap remark of `40c5bd7`, including its degenerate branch; behaviours mixed within a run and
the two adversaries; real inner brackets and three levels; the comparison of `C_max` with the
non-adaptive *lower* bound (§2.9).  *Where we overlap the numbers agree:* `C_max`, the plain bracket, the
hinted lower bound and the flat-instance trajectory (§3.3), to every published digit.  My literal runs
with their profile families (flat, cones, plateau-then-cone, dips around the critical radius, the
staircase, the 2-periodic profile, random walks) show, like theirs, no failure of the good event with
the theorem's `K` and no violation.

### 3.8 How to re-run (from `experiments/science/ws_R6/`; `OMP_NUM_THREADS=1`)

    python3 campaign.py A_small 1600 11 2        # likewise A_ties 500 12, A_medium 500 13 (and 44 2), D_2L 240 16,
                                                 # B_reducedK 400 14, B_invalid 400 15, B_lazy 60 19 and 200 20
                                                 # (seed 18 was run with rung costs 10^l), D_2L_off 300 17, A_small 64 1
    python3 campaign.py MUT_neg_tol 48 7 2       # mutations: MUT_noharper, MUT_maxform, MUT_close_at_no, MUT_q_no_eta
    python3 capcorner.py 1500 41                 # seeds 41, 42, 43
    python3 e2e.py 600 21 1 ; python3 e2e.py 400 22 16 ; python3 three.py 40 61 6
    python3 adversarial.py <cell 0..6> <ineq|count|calls|cap|mbar|cost> <evaluations> <seed> ; python3 capsearch.py 71 200
    python3 everyn.py 1.0 0.5 4000,16000 ; python3 separation.py 1.0 250,...,8000 ; python3 flat_exact.py 1.0 1000 0.80
    python3 check_tail_lemmas.py ; python3 check_K4cd.py ; python3 tau2.py ; python3 crosscheck_lb.py
    python3 make_section3.py                     # every number of section 3.2, 3.4, 3.6 from the data files
    cd /home/user/MetricChain && lake env lean /home/user/MetricChain/experiments/science/ws_R6/lean/R6Axioms.lean    # and R6Axioms2.lean

Campaigns are stopped by a time limit when the machine is loaded; the run counts above are those of the
data files in `data/`.  `NOTES.md` records what was run in which order, including what was discarded.



## 4. Prior art, with a search log

The object of this workstream is a proof, not a novelty claim; I looked only at the cited inputs and
made one generic search for the result itself.  Searches on 25 Nov 2026, generic queries, no project
information sent.

| query / page | what I read | level |
|---|---|---|
| "Harper vertex isoperimetric theorem hypercube initial segments simplicial order minimize neighbourhood Hamming ball statement" | the statement as quoted by the search tool from Räty, arXiv:1806.11061, and Przykucki–Roberts, arXiv:1808.02572: for `A ⊆ Q_n` and `B` the initial segment of the simplicial order with `|B| = |A|`, `|N(A)| ≥ |N(B)|` (also in the closed-neighbourhood form); initial segments of ball size are balls | [search snippet]; Harper 1966 not retrieved |
| "Kaas Buhrman 1980 Mean, median and mode in binomial distributions median between floor np and ceil np" | bibliographic data (Statistica Neerlandica 34(1), 13–18); a 1978 preprint statement that an integer within `min{p, 1−p}` of `np` is a median; the `⌊np⌋ ≤ m ≤ ⌈np⌉` form is attributed to the paper by secondary sources | [search snippet]; the paper itself not read |
| arXiv math/0611285 (Mathé–Novak, *Simple Monte Carlo and the Metropolis algorithm*) | "adaptive methods are much better than nonadaptive ones … the curse of dimension (for nonadaptive methods) can be broken by adaption", for integration with respect to an unknown density, by a Metropolis ball walk, "for certain classes of inputs" | [abstract], through a fetch tool |
| "adaptive versus non-adaptive query complexity estimating partition function Lipschitz function Hamming cube exponential separation isoperimetric layer cake algorithm" | nothing on this problem (junta testing, partition learning, nearest-point search in the cube) | [search snippets] |

*Assessment.*  The two cited combinatorial inputs are standard and are used in the form in which they
are known: Harper [K, search snippet; verified by computation on all subsets of `Q_m`, `m ≤ 4`, §3.5];
binomial median [K, attribution unverified; verified by computation for `m ≤ 4000`, §3.5 — the proof
needs only *some* constant in place of `½`].  On novelty I have nothing to add to
`docs/prior_art/L7_query_complexity.md` and to the referees' logs: the qualitative phenomenon is in
Mathé–Novak; the exact exponents and the algorithm were **not found**, at the level of abstracts and
search summaries, which is not "new".  The finite-`n` separation of §2.9 is a computation with the
programme's own theorems; I did not search for it and make no novelty claim.

## 5. What I did not settle

1. **Three or more nested levels, end to end.**  My runs with real inner brackets are on cubes of
   12–13 coordinates (two levels) and 9–10 coordinates (three levels, 19 outer runs), where the
   algorithm can only be tested for logic (an inner bracket costs more than enumerating its fibre).
   With the constants of the theorems a two-sample bracket becomes cheaper than enumeration at about
   30–40 fibre coordinates for `u = 1` and 80–150 for `u = 2` (computed with `everyn.k0_cost` for
   accuracies `0.5` and `2`), where a single bracket already costs `e^{17}`–`e^{26}` (`u = 1`) evaluations
   or more, and a level above it needs `e^{n_oa}` outer points: there is no size at which the nested
   algorithm can be *executed* with real randomness at every level and with sampling cheaper than
   enumeration.  Referee R8's three-level runs on `Q_9, Q_10` have the same limitation.
   The composition is therefore certified only by the interface "bracket procedure" (which I checked)
   and by the exact flat-instance computation of R8 (which I did not repeat for three levels).
2. **A rate.**  No explicit `o(n)` for Theorems 11.54/11.58, and no explicit `n₀(η)` (§2.6, §2.9).
3. **The Lean proofs** line by line; **Theorem 11.25(d)** (asymptotics of the lower bound) and the
   closed forms of the two sums in `cube_exact_dip_randomized`, beyond what my tables use (the hinted
   and non-adaptive lower bounds are *computed* from the exact sums in §2.9, and agree with the
   engineering division's hinted column).
4. **Monotonicity in `n`** of the separation of Corollary R6.2 (observed on the grid only).
5. **Outer landscapes with real fluctuations and real inner brackets** beyond explicit cubes with
   `n_o ≤ 8`.  With a simulated inner oracle the run depends on the instance only through the law of
   `W` (remark of `40c5bd7`; I checked both directions of its Harper argument), and my class
   instances — radial, increments anywhere in `[−u, u]`, whole shells — cover those laws up to partial
   shells; laws with partial shells are not covered by my simulated runs.
6. **The frequency of the good event from below**: with the constants of the theorems it never failed
   in my runs; with `K` reduced it fails, and I report the frequencies, but I did not test whether the
   bound `δ` is anywhere near tight (it is a union bound and is not).
7. **Theorem 11.51** (radial class) was outside my list and not examined.

## 6. The three most promising next steps

1. **Machine-check the deterministic core of Theorem 11.56** — the statements that hold "for every
   run": the closing radius of a level that is left (Step 5), the sample sizes (Step 6), the lowered
   cap of §2.8, the width (Step 4).  They are statements about an abstract run — a finite sequence of
   passes `(j, M, N)` obeying the update rules of §2.1, with tables `|B|, E, T` as parameters — and use
   no probability and no geometry beyond monotonicity of the tables.  This is a formalisation of a few
   hundred lines, it removes the sentence "nothing in the count of evaluations is machine-checked" for
   the part of the count that was wrong five times, and it leaves outside Lean only Chernoff, Harper
   and the two tail lemmas.
2. **State the finite-`n` separation as a theorem with numbers**, after an independent recomputation
   (the engineering division has every ingredient): the least `n`, for each `u`, at which a certified
   adaptive upper bound is below the non-adaptive lower bound, with the design (`φ`, ladder, `λ, η, θ`)
   optimised for that purpose and with the lowered cap.  It turns "exponents differ" into a statement
   a reader can check at `n = 1400`.
3. **A rate for the recursion** (`T_k − θ_hint ≤ C/k²` is what the numerics suggest), or a different
   construction at bounded accuracy that does not halve the accuracy at every level: either would
   give the first explicit `o(n)` and decide whether `e^{nh + O(n^{3/4})}` is an artefact.

## 7. Requests

**To the theory division** (each can be sent as it is):

* **R6-T1 (cap remark, `40c5bd7`).**  In the proof of the remark after Theorem 11.56 the sentence
  "(If `r† < Δ`: a pass with `2^{n_o}q < 1` has an empty tail.)  So at level `j` the size is doubled only
  below `M‡`" does not cover the pass with `M = M‡ = K2^{n_o}/(1−η)` exactly (`η = ½`), where
  `2^{n_o}q = 1`, `r = 0`, `tail = s_j2^{−n_o}E_0`.  In 4 500 runs of `capcorner.py` that pass failed to
  close 1 255 times (all with `r† ∈ {0, −1}`), and in 1 133 runs the largest sample was exactly `2M‡`.  The
  statement survives: for `r† ≥ 1`, `E_0 ≤ E_1/(n_o+2)` and `λ ≤ 1` give `tail < s_{j−1}2^{−n_o}E_{r†} ≤ θe^bℓ`;
  for `r† ∈ {0, −1}`, `M† ≥ M‡` and the cap is `2e^λM†`.  Please add these lines and say that `λ ≤ 1` is
  used here (erratum m3 of `K_REPORT.md` calls it unused).
* **R6-T2 (§11.18 text).**  (i) line 3649: the abort test must precede the inner call, as in line
  3986; (ii) line 3707: add the reference query and the rung-0 queries, start the sum at `l = 1`;
  (iii) line 3689: add the case `s_je^{−x} < s₀`; (iv) lines 3804–3810: admit a tuple only from its own
  `n₀` on, or replace the assembly by Proposition E of `K_REPORT.md`, which needs neither `n₀` nor left
  limits.
* **R6-T3 (a finite-`n` statement).**  Consider adding to §11.19, after an independent check, the
  comparison of `C_max` with the *non-adaptive lower bound* of Theorem 11.45(b) at the same accuracy
  (§2.9): crossover `n = 1400` (`u = 1`), `540` (`u = 2`), `4700` (`u = ½`) for the design of
  `K_REPORT.md` §6.4.  The present text compares with the plain bracket, which is an upper bound.
* **R6-T4.**  Is there a rate for `T_k → θ_hint`?  Even `T_k(g) − θ_hint(g) ≤ C(u, g)/k` would make the
  `o(n)` of Theorems 11.54/11.58 explicit.

**To the engineering division:**

* **R6-E1 (recompute §2.9).**  *Motivation:* a certified finite-`n` separation between adaptive and
  non-adaptive algorithms.  *Formulation:* for `u ∈ {½, 1, 2}` and every `n` in a window around the
  crossover, compute `C_max` of Theorem 11.56 with base brackets inside (your evaluator has it: the
  column "cap `C_max`"), with and without the cap of the `40c5bd7` remark, and
  `LB_na = (1−2δ)2ⁿ/|B(n, R−1)|`, `R` the least radius with
  `n ln(1+e^{−u}) + uR − ln T_n(R) > x_out`.  *Inputs:* the design of your ENG-RES-0008; then a search
  over `(φ, λ, η, η′, θ, ladder)` minimising the least `n` with `C_max < LB_na`.  *Expected output:* that
  least `n` per `u`, and whether the inequality is monotone in `n` beyond it.  *Validation:* my values
  `ln C_max = 154.0`, `ln LB_na = 155.0` at `u = 1`, `n = 1400`, `φ = 0.5` (files
  `experiments/science/ws_R6/data/separation_K64_u*.jsonl`).  *Stopping:* one window of 200 sizes per
  `u`.  *Resources:* seconds per cell at `n ≤ 5000`.
* **R6-E2 (the abort rule).**  Your literal runs report "aborted: 0".  With an invalid inner
  behaviour that returns the rung-0 bracket at every rung but the last (so that every refined point
  reaches the dearest rung) and rung costs growing by `e^{80}`, 149 of my 260 runs stop on the query
  budget, and the cost stays below `C_max` only because the test precedes the call.  A harness for
  the "bracket procedure" interface should contain such a behaviour; it is the only test of the
  sentence "the cost bound holds always".

## 8. What a hostile referee would attack first

In this order.

1. **"The theorem's content is the count of evaluations, and the count is not machine-checked."**
   True, and said by the authors.  What is in Lean is the analysis of the recursion and four algebraic
   identities; the algorithm, its events and its cost are ten pages of paper with five retracted
   predecessors.  The defence is redundancy, not formality: the accounting has now been derived
   independently three times (R7 and R8 inside the theory division, this review outside it) with
   identical constants, implemented independently five times (workstream K, the coordinator, R8, the
   engineering division, this review) — the three whose numbers I could compare (workstream K, the
   engineering division, this review) agree to every published digit — and attacked with mutations
   that each implementation detects.  A referee who does not accept that will ask for the
   deterministic half of the count in Lean (§6, step 1) — a reasonable demand and a feasible one.
2. **"Exponent `h` is a limit of families of growing depth; there is no algorithm, no rate, no
   finite-`n` content beyond two levels."**  Also true.  For a target `h + 2η` the proof stacks about
   `ln(a/h)·a/η` bounded levels, with inner accuracies `ε/2^j`, on top of an unspecified number of
   extensive levels; the "polynomial" prefactors at fixed `η` are of size `exp(Θ(η⁻²))` (**[H]**, my
   estimate: `m ≈ 1/η` levels whose constants `K_j ∝ 4^j` multiply along the chain) and the `o(n)` is
   heuristically `n^{3/4}` (theirs).  The honest headline is "*at the exponential scale* adaptivity recovers the
   hinted exponent"; the only certified statement at a finite size is the two-level one of §2.9
   (separation from non-adaptive algorithms from `n = 1400` on at `u = 1`), and it is about two levels
   and exponent `≈ a/2`, not about `h`.
3. **"Nobody has run it."**  With the constants of the theorems an inner two-sample bracket is cheaper
   than enumeration only from 30–40 coordinates on (`u = 1`), where one bracket costs more than `10⁷`
   evaluations, so every end-to-end run with real inner randomness (workstream K, R8, mine) is at sizes
   where sampling is dearer than enumeration; every large-size run uses a simulated oracle or
   expectations.  What links the levels is one definition ("bracket
   procedure": cost bound in every run, validity and width with probability `1 − δ′`), and the proof
   uses nothing else — but a referee will note that the composition of three levels has been
   exercised only on `Q_9`, `Q_10` (R8; here: 19 outer runs, §3.4) and at the flat instance (R8).
4. **"Worst case against one instance."**  The lower bound is at the zero function; the algorithm's
   own worst instance is not the zero function (engineering division, ENG-RES-0008), and the cost
   table that the theory report quoted until `40c5bd7` was a best case.  This is now corrected in the
   text; it does not touch a theorem.
5. **"Harper's theorem and the binomial median are quoted from memory."**  They are standard and are
   used in their standard form; both were verified by computation here and by R8.  A final version
   should cite page and theorem number.
6. **The abort rule.**  A referee who reads Theorem 11.52 as printed (abort *after* the budget is
   exceeded) gets `bound + one inner call`; and one who suspects that the rule is decorative should be
   shown §3.2: with an invalid inner behaviour and a dear last rung the run *does* exceed the budget
   unless it is stopped, in 149 of 260 runs.

What a hostile referee would **not** find: an error in the validity of the bracket (it was never in
doubt), a wrong constant in the count, a tolerance entering the wrong place (the one thing that went
wrong five times), or an instance on which the claimed bound fails.
