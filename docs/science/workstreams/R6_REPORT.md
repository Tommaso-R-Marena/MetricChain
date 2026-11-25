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
* **Not done**: three nested levels with real inner brackets; a run with real inner brackets at sizes
  where sampling is cheaper than enumeration (impossible with the constants of the theorems below
  `n ≈ 10³`, see §5); Theorem 11.51; a second reading of the lower bound's asymptotics.

## 1. Verdicts in one paragraph

**The cost accounting of the nested algorithm stands.**  I found no critical and no major error in
Theorems 11.52, 11.54, 11.56, Proposition 11.57 and Theorem 11.58: an accounting written from scratch
reproduces the published one constant by constant (the closing radius, `M ≤ 8Je²M†` resp. `M̄`, the
count `16KJe²e^x` resp. `c_η⁻¹e^λνe^x` in which the two factors `e^b` cancel, the per-rung call
bound); the five wrong accountings of `DEAD_ENDS.md` D45 are not repeated in another guise (§2.5); an
independent implementation violated no claim in **5 930 literal runs** with the constants of the theorems
— including, for the first time, **1 020 runs with invalid inner answers** (the statements "for every run,
on or off the good event" hold there, and the abort rule keeps the cost below `C_max`), the algorithm
of Theorem 11.52 itself at sizes where levels are left as negligible, and 1 200 runs with real
two-sample inner brackets (§3) — and it reproduces to every published digit numbers of the engineering
division that I had not seen when I wrote it (§3.3).  **What I add:** (i) seven minor findings, each
with its repair (§2.7); the only one that touches a proof is an uncovered pass in the new cap remark of
`40c5bd7`, which I close (§2.8); (ii) an **every-`n` statement with no `o(n)`**: the two-level algorithm
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
| Theorem 11.52 (one more level; Algorithm 2L) | **proved** (four minor gaps, all closed: m1–m4) | own derivation before reading; 2 400+ own runs of 2L |
| Theorem 11.53 (recursion → hinted exponent) | **[V]**: statement read against the paper, compiled, axioms printed | `lean/R6Axioms.lean`; the Lean *proof* not read |
| Theorem 11.54 (extensive accuracies) | **proved**, given 11.25(a) [V], 11.53 [V], 11.44/Prop. 11.46 or K0 [P], Harper, Chernoff [K] | assembly re-derived in both forms (left limits; Proposition E) |
| Lemma 11.55 = K.4 | **proved**, given the binomial median [K] | re-derived; exact tables `m ≤ 4000` |
| Theorem 11.56 = K1 (Algorithm 2L⁺) | **proved** | Steps 4–7 derived before reading, 1–3, 8, 9 after; 3 500+ own runs |
| Remark after 11.56, "cap `2max{e^λM†, M‡}`" (**`40c5bd7`**) | **proved with a gap that I close** (m7) | re-derived; checked in every run |
| Proposition 11.57(a) = K0 | **proved** | re-derived; cost reproduced numerically for `d ≤ 16 000` |
| Proposition 11.57(b) = K2, (c) | **proved** (in the corrected form `T′(ξ) = min(T(ξ), T′(0))`) | re-derived, including accuracy arithmetic and (E0′) |
| Theorem 11.58 = K3, Corollary K3′ | **proved**, given the above, 11.25(a),(d) and (R) = `exactRec_reaches_hint` [V] | iteration re-derived; `two_rung_bound` [V] |
| Theorem 11.51 (radial class) | not examined | — |

## 2. Precise statements, proofs, findings

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
left as negligible has `s_{i+1}q_i ≤ e s_i·2K/M_i^neg = e^bℓ/J`.  With `s₀ ≤ ℓ` and `tail ≤ e^Gℓ`:
`U/ℓ ≤ 1 + 4(J+1)e^{b+1}·[populated share] + e^b + e^G`, hence the width.

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

