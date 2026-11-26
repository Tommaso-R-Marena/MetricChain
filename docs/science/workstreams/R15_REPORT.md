# Workstream R15 — independent review of four statements the theory division asked us to review (theory commit `f7df44f`)

*Written 2026-11-26 by the R15 agent.  Object: the read-only export of the theory tree at `f7df44f`
(`<EXP>` below); request: `THY-RES-0012`, "Requests" 1 and 3, §1.2 and "Requested response".
Everything here is model-relative mathematics on finite sets; no physical claim is made or reviewed.
Scripts, logs and running notes: `experiments/science/ws_R15/` (`NOTES.md` has the step-by-step record).*

**Four kinds of checking, kept apart throughout.**  **review** = I re-derived the statement on paper from its
hypotheses; **replication** = I recomputed it with code of my own, written from the statement (nothing imported
from the theory division's or the coordinator's code); **re-run** = I ran their code; **read only** = I read it
and did neither.  Labels: **[V]** machine-checked (declaration named), **[P]** paper proof given here (with what
was checked numerically), **[K]** known (with the reading level), **[N]** numerical evidence only, **[C]**
conjecture, **[H]** heuristic.

**Headline.**  Nothing false was found in the four statements, in the necessity argument of Proposition
11.113(d), or in the Lean statement.  There is **no critical and no major finding**.  There are twelve minor
findings — conditions to add and sentences to make precise — each with a replacement text (§1), and six
additions of ours that came out of the review (§1.3): a finite-depth form of the one-site count; a bound for the
nested sampler with `t_f` in place of `2t_f`; an exact criterion for the "most frozen site" rule in terms of the
penalty at a site against the free-energy cost of changing it; the structure of the best vertex for the lower
end; a form of the necessity bound that grows like `ln(1/δ)`; and the observation that along the hidden
direction the event `S` of the outline is a single interval.  All their numbers that we recomputed agree with
ours to the digits printed.

---

## 0. Verdict table

| # | statement (theory report at `f7df44f`) | verdict | how checked |
|---|---|---|---|
| 1a | Prop. 11.18e(b′)(i): `P_g(a` not evaluated`) ≤ δ` for every `a`, `g`; `E\|Q(g)\| ≥ (1 − δ)\|X\|` | **correct** (uses that the returned upper end of `ln Z` / lower bound of the minimum is finite — it is, by the task of (a); say so) | review; replication of the "every randomised algorithm" quantifier by linear programming in a finite model |
| 1b | … "attained by skipping one uniformly random state with probability `kδ`" | **correct with conditions to add**: `kδ ≤ 1`; for `ln Z` the bracket returned after a skip must be at least `ln 2` wide (for the minimum any slack `≥ 0`).  The coordinator's first reading (SCI-RES-0016 §3) is right.  A trivial mixture attains the bound with no condition | review; replication (exact arithmetic, ties included) |
| 1c | … "the saving of (b) … comes from evaluations outside the ball alone" | **correct; the argument is not in the text** — it follows from the *proof* of (i) plus unisolvence, not from its statement | review; replication of the unisolvence step |
| 1d | harness XI.22(d) | tests **`ln Z` only, width 3.0** (≥ `ln 2`), one needle and one flat instance per `k`; no minimum, no narrow width | read; re-run (survived) |
| 2a | Prop. 11.18f(a): cost number, product formula, mean penalty `p^kΓ` "exactly" | **correct**, for every `0 ≤ k ≤ m`, arbitrary constants, and in fact for every allocation of level `k` | review; replication |
| 2b | 11.18f(b): convexity/concavity, gradients, the "iff" for `U` | **correct** (the "iff" is a fixed-point condition: the tilted law is that of the allocation itself; ties allowed) | review; replication |
| 2c | 11.18f(b): "the minimum of `L` is attained at a vertex" | **correct; "which vertex" can be said**: an *ordering* vertex; not every vertex is a local minimum; for independent sites and exchangeable constants "most frozen first" is the global minimiser; in general a search | review; replication (all 59 049 vertices of small instances) |
| 2d | 11.18f(c): first-order rule; `γ_i = Γ(R_i) − Γ(R_i ∖ {i})` | **correct with a condition to add**: a linear order of the sites (ties broken); with ties read as "`p_j ≥ p_i`" the formula double-charges.  First order only — criterion in §3.5 | review; replication |
| 2e | 11.18f "Numbers" | **correct**: all six quoted pairs reproduced (and two more computed) | replication; re-run |
| 3a | Prop. 11.113a(a), (b) | **correct** | review; replication (11 identities by enumeration on 7 instances) |
| 3b | 11.113a(c): the bracket with `2t_f + ρ̄t`, `ln(6/δ)` | **correct with a condition to add** (the sampling scheme); **can be sharpened** to `t_f + ρ̄t` at the same `ln(6/δ)` | review; replication (168 000 runs) |
| 3c | … "the term `2t_f` cannot be dropped" | **correct** as "a free term cannot be dropped"; the coefficient 2 can | replication |
| 3d | 11.113a(d): limit, "no algorithm does better in order", "`4/(E_qρ)²` proposals per evaluation" | **correct with two small conditions**: the limit carries `ln(6/δ)`, not the `ln(2/δ)` of 11.113(c) (factor 1.14 at `δ = 0.05`); the lower bound needs the *inner* sampler fine-grained and is "in order" for inner brackets of bounded width | review |
| 3e | the coordinator's variant `t_f(1 + \|W̄_in − ½\| + t) + ρ̄t` | **correct** (and dominated by `t_f + ρ̄t`) | review; replication |
| 4a | `ratio_expected_queries_ge_mixed` against Cor. 11.114(c) | **faithful**: every hypothesis of the theorem is in the sentence or in the preamble; nothing more is claimed than proved; the sentence omits "on `r`, in expectation" | read only (**not compiled**: `BoxClass.lean`, `BoxRatio.lean`, `BoxAdditions.lean` are absent from our tree) |
| 4b | Cor. 11.114(d) | **correct as an order statement, with conditions to state**: `ε ≲ 1`, no heavy single state, `U_M, V_M > 0` in both macrostates.  The theorem gives a *sum* over macrostates, within a factor 2 of the `max` | review; a numerical companion on 400 random boxes |
| 5a | Prop. 11.113(d), the necessity argument (THY-RES-0012 §1.2) | **correct** — no gap found; four small precisions | review; replication of both probabilistic steps by exact enumeration |
| 5b | the table (Pinsker bound, `N_TV`, `N_KL`) | **correct**: all fifteen numbers reproduced | replication; re-run |
| 6 | Prop. 11.18e(b′)(ii), the outline (conjecture) | **no false step found on the cube at order two**; the unwritten steps look routine; beyond that setting the pairing itself fails | review of each step; replication of the combinatorial steps in exact arithmetic; density ratio measured; re-run of `pairing_check.py` (identical output) |

---

## 1. Findings by severity, with replacement texts

### 1.1 Critical: none.  Major: none.

### 1.2 Minor (twelve)

**m1 — Prop. 11.18e(b′)(i), "It is attained by skipping one uniformly random state with probability `kδ`."**
True for the task of (a) only when `kδ ≤ 1` and the bracket returned after a skip is wrong for at most one
skipped state per instance.  Written out (§2.3): the failure probability on an instance is
`δ·#{a :` the output returned without `a` is invalid`}`.  For the minimum the count is at most one for every
slack `w ≥ 0`; for `ln Z` with the bracket `[ln Z_seen, ln Z_seen + W]` it is at most one iff `W ≥ ln 2`, and
`min(k, ⌈1/(1 − e^{−W})⌉ − 1)` in the worst case otherwise (two equal states: `2δ`; `k` equal states and
`W < ln(k/(k − 1))`: `kδ`).  The harness uses `W = 3`.  *Replacement:*

> … and `E|Q(g)| ≥ (1 − δ)·|X|`, `|Q(g)|` the number of distinct states evaluated (the limit `D → ∞` uses that
> the returned upper end of the bracket of `ln Z`, or the returned lower bound of the minimum, is finite; a run
> that returns no finite bound counts as a failure).  The bound is attained on every instance, for every width
> and every `δ`, by the trivial mixture "with probability `δ` evaluate nothing, otherwise everything".  For
> `kδ ≤ 1` it is also attained by skipping one uniformly random state with probability `kδ`, provided the
> bracket returned after a skip is wrong for at most one skipped state: for the minimum, the lower bound
> "least evaluated value minus `w`" with any `w ≥ 0`; for `ln Z`, the bracket `[ln Z_seen, ln Z_seen + W]` with
> `W ≥ ln 2` — for `W < ln 2` its failure probability is `δ·min(k, ⌈1/(1 − e^{−W})⌉ − 1)` in the worst case, `2δ`
> on two equal states (harness XI.22(d): `ln Z`, `W = 3`).

**m2 — Prop. 11.18e(b′)(i), last sentence ("The saving of (b) … therefore comes from evaluations outside the
ball alone").**  Correct, but not a consequence of (i) as stated ((i) is about classes closed under adding
every function; on several sites with `m ≤ n` the class is not).  It follows from the proof of (i) with a
Lagrange function of the ball in place of the needle (§2.4).  *Replacement:*

> The saving of (b) on more than one site comes from evaluations outside the ball.  An algorithm that
> evaluates only inside a fixed unisolvent set `B` — the ball, say — has `P_g(a` not evaluated`) ≤ δ` for every
> `a ∈ B`, hence `E|Q(g)| ≥ (1 − δ)·N_ball`: let `h_a` be the function of order below `m` that is `1` at `a` and
> `0` on the rest of `B` (it exists because `B` is unisolvent); if `a` is not evaluated the run is the same on
> `g` and on `g + t·h_a`, and `min(E₀ + g + t·h_a) → −∞` as `t → −∞`.  A function of order below `m` cannot hide
> from a random point; inside a unisolvent set it can, as a needle does.

**m3 — Prop. 11.18e(b′)(i), hypothesis.**  "one site with `k` states, or `m > n`": the first is the case
`n = 1` of the second (and needs `m ≥ 2`).  The argument uses much less than closure under every function:
only that `g − D·1_a` stays in the class for arbitrarily large `D`, for every state `a` (a box class without a
floor is such a class).  *Replacement:* "Where, for every `g ∈ 𝒢` and every state `a`, the class contains
`g − D·1_a` for arbitrarily large `D` — in particular where it is closed under adding every function, `m > n`
(one site with `m ≥ 2`) — …".

**m4 — Prop. 11.18f(c), the formula `γ_i = Γ(R_i) − Γ(R_i ∖ {i})`, "`R_i` the sites at least as mobile as `i`".**
Exact if the sites are *linearly* ordered and `R_i` is "`i` and the sites after it" (the harness does this,
breaking ties by index).  Read as `R_i = {j : p_j ≥ p_i}` with ties, tied sites are each charged the constants
they share: in the first example of "Numbers" this gives `γ = (1, 1, 1, 1, 0, 0)`, sum `4.0` against `Γ = 2.0`,
and `(U, L) = (0.068, 0.025)` instead of `(0.030, 0.014)` — a valid cover, not an allocation.  With ties "its
least probable sub-pattern" is not unique, and the two ends disagree already at first order: in that example
the least `U` over *all* allocations is `0.0259` (the four tied frozen sites share), below the vertex's
`0.0298`.  *Replacement:*

> … with the sites in a linear order by `p_i` (ties broken in any fixed way) and `R_i` consisting of `i` and
> the sites after it, `γ_i = Γ(R_i) − Γ(R_i ∖ {i})`.  Where sites are tied the first-order optimum is not
> unique: the upper end is least when the tied sites share a constant, the lower end when one of them takes it.

**m5 — Prop. 11.18f(c), range of validity of "charge every constant to its least probable sub-pattern"; and
THY-RES-0012 §3.2 item 4 ("the constants of subsets that contain an interior residue belong on it").**  The
rule is first order, and is labelled so.  What is missing is the condition under which it stays right when the
constants are not small — the question the coordinator put to this workstream.  §3.5 gives it; in one line:
**the floor model sees the net cost `f_i − γ_i`** (`f_i = ln((1 − p_i)/p_i)` the free-energy cost of changing
site `i`, `γ_i` the penalty it carries), **the ceiling model sees `f_i + γ_i`**.  This is the finding with the
largest practical weight: the rule can raise the upper end above that of equal shares without bound, while it
cannot raise the lower end by more than the factor `m`.  *Text to add after (c):*

> *Beyond first order* (independent sites, level 1; `sp(z) = ln(1 + e^z)`).
> `U = Σ_i [sp(γ_i − f_i) − sp(−f_i)]` and `L = Σ_i [sp(−f_i) − sp(−f_i − γ_i)]`.  A site with penalty `γ_i`
> costs between `max(p_iγ_i, γ_i − ln(1/p_i))` and `p_i(e^{γ_i} − 1)` at the upper end — beyond `ln(1/p_i)` the
> penalty is paid nat for nat — and at most `min(p_iγ_i, −ln(1 − p_i))` at the lower end.  The vertex of (c)
> minimises `U` iff in every `T` the charged site still has the largest `f_i − γ_i` of its `T`; the minimiser
> of `U` equalises `f − γ` over the sites that share constants.  At the lower end every allocation of level
> `k` is within the factor `C(m, k)` of equal shares, for any law.

**m6 — Prop. 11.18f(b), "the minimum of `L` is attained at a vertex".**  True.  The text does not say which,
and a reader may take "a vertex" for "any vertex" or for "the vertex of (c)".  *Replacement:*

> … while **the minimum of `L` is attained at a vertex — at an ordering vertex: every constant charged to the
> first `k`-subset of its `T` in one linear order of the `k`-subsets** (the achievable charges form the base
> polytope of a polymatroid).  Not every vertex is a local minimum — a vertex is one iff every constant sits
> on the `k`-subset of its `T` that is least often changed under the tilted law `P·e^{−pen}` of the vertex
> itself — and there can be many local minima.  For independent sites and exchangeable constants the order
> "most frozen first" is the global minimiser; in general finding the best order is a search (it contains a
> minimum-weight hitting-set problem).

**m7 — Prop. 11.113a(c), the sampling scheme is not stated; (c) and (d) presuppose different ones.**
Hoeffding's inequality needs sample sizes that are fixed, or determined by something independent of the
averaged values.  (c) reads "`N_f` proposals … and `N` evaluated draws"; (b) says "evaluate `E` only if
accepted", which makes `N` random (`≈ ρ̄N_f`); (d) asks for `4/(E_qρ)²` proposals per evaluation, which is
impossible if every accepted proposal is evaluated.  The bound holds in all the natural readings but one
(§4.3).  *Replacement for the first sentence of (c):*

> (c) Let `N_f` be fixed in advance, the proposals independent draws of `q`, and let the proposals that are
> evaluated be chosen among the accepted ones by a rule that looks at the acceptance indicators only — all of
> them, the first `N`, or an independent stream of `N` accepted draws; `N` is the number evaluated.  Then,
> with probability at least `1 − δ`, … (three applications of Hoeffding's inequality, the one for `W̄_in`
> conditionally on the acceptance pattern).  The bound is not proved if proposals are drawn *until* `N` have
> been accepted (`N_f` is then a stopping time and `ρ̄` is biased, of relative order `1/N`), nor for a
> stopping rule that looks at the running bracket.

**m8 — Prop. 11.113a(c), "`2t_f`".**  The factor 2 is not needed (§4.4): with the same three events and the
same `ln(6/δ)`, the half-width is `A·(t_f + ρ̄·t)`.  *Replacement:*

> `| Z(E) − Z(m₊) − A·(β̄ + ρ̄·W̄_in) |  ≤  A·( t_f + ρ̄·t )`  (Hoeffding's inequality for `β`, for `β + ρ` — the
> two ends `Z(e₊)`, `Z(e₋)` of the inner bracket, both variables in `[0, 1]` — and for `W_in`; the error of
> the free part, `(E_qβ − β̄) + (E_qρ − ρ̄)·μ`, is affine in `μ = E W_in ∈ [0, 1]`, so it is at most the larger
> of its values at `μ = 0` and `μ = 1`).  A free term cannot be dropped altogether; it costs proposals only —
> about `1/(E_qρ)²` proposals per evaluation for the two errors to balance.

**m9 — Prop. 11.113a(d), "As `N_f → ∞` the half-width is `(Z(e₋) − Z(e₊))·t`, that of Proposition 11.113(c)
for the inner sandwich".**  `t` carries `ln(6/δ)`; 11.113(c) carries `ln(2/δ)`.  *Replacement:* "… that of
Proposition 11.113(c) for the inner sandwich up to the factor `√(ln(6/δ)/ln(2/δ))` (`1.14` at `δ = 0.05`),
which disappears if a vanishing share of `δ` is given to the two free events; and, where the inner sampler is
fine-grained and the inner bracket of bounded width, no algorithm does better in order over the box
`{e₋ ≤ E ≤ e₊}`."  (The arithmetic "about seven times" of THY-RES-0012 §2.3 becomes about six with the stated
split.)

**m10 — Prop. 11.113a, comparison with the plain sampler (asked by the coordinator; not in the text).**
*Text to add:*

> At equal numbers of evaluations the bound of (c) is narrower than that of Proposition 11.113(c) iff
> `2√(N/N_f) + ρ̄ < κ(δ) := √(ln(2/δ)/ln(6/δ))` (`0.855`, `0.878`, `0.910` at `δ = 0.1, 0.05, 0.01`): never for
> `ρ̄ ≥ κ`; otherwise for `N_f > 4N/(κ − ρ̄)²`, at least `5.2 N` proposals at `δ = 0.05`.  If every accepted
> proposal is evaluated (`N = ρ̄N_f`), only for `ρ̄ < (√(1 + κ) − 1)² = 0.137`.  (With `t_f` in place of `2t_f`:
> `√(N/N_f) + ρ̄ < κ`, and `ρ̄ < 0.316`.)

**m11 — Prop. 11.113(d), the necessity argument: four precisions** (the argument is right; §6).  (i) "the
values of `ln Z` under `w` and under `w′` differ by `2ε`, so … total variation at least `1 − 2δ − o(1)`":
"within `ε`" is a closed condition and `q(D)` fluctuates, so `w′` should be taken a little beyond
(`c + w′ = e^{2ε + η}(c + w)`, `η → 0`); the bound is unchanged in the limit.  (ii) `w′ ≤ 1` needs
`ε ≤ ½·ln((e^Δ + 1)/2)` at `w = c/(1 + 2c)` (true in all five rows of the table; `0.0153` against `0.01` in the
first).  (iii) "`≈ (1 − 2δ)²·sinh²(Δ/2)/ε²` … for small `ε`" means `ε ≪ (1 − e^{−Δ})/4`: in the first row of
their own table the exact Pinsker bound is `5.7` where the formula gives `7.4`.  (iv) "fine-grained" is, with
its quantity, `Σ_x q(x)² ≪ ε²/sinh²(Δ/2)`: the sampler must have many more effective states than the count
itself.  *Replacement for the display and the sentence before it:*

> Take `w′` with `c + w′ = e^{2ε + η}(c + w)` for a small `η > 0` (possible while `e^{2ε + η} ≤ (e^Δ + 1)/2` at
> `w = c/(1 + 2c)`): once the fluctuation of `ln Z` on the random member — of standard deviation
> `√(w(1 − w)·Σ_x q(x)²)/(c + w)` — is small against `η`, an algorithm that is within `ε` with probability
> `1 − δ` on every member tells the two laws of bits apart with total variation at least `1 − 2δ − o(1)`, and
> by Pinsker's inequality, in either direction of the divergence,
>
>     N  ≥  2(1 − 2δ)² / min(KL(w‖w′), KL(w′‖w))   ≈   (1 − 2δ)²·sinh²(Δ/2)/ε²     for ε ≪ (1 − e^{−Δ})/4.

**m12 — Corollary 11.114(c), (d).**  (c): the sentence does not say where and in which sense the evaluations
are forced.  (d): the regime and the hypotheses of the upper bound are implicit, and "max" hides that the
machine-checked lower bound is a sum.  *Replacements:*

> (c) … pairwise disjoint such sets, of either kind and in either macrostate, force of every randomised
> algorithm that is `(ε/2, δ)`-correct for the log-ratio on the box, **at the instance `r` at which they are
> heavy, `(1 − 2δ)` evaluations each in expectation.**
>
> (d) Hence, for `ε ≲ 1`, where no single state has that much dip or bump weight and `U_M, V_M > 0` in both
> macrostates, the cost … is, up to a factor depending on `δ` only and an additive constant, [the display].
> With `a_M = W_M(lo)/W_M − 1` and `b_M = 1 − W_M(hi)/W_M`, for `ε ≤ 1`:
> `(1 − 2δ)·(max_M (a_M + b_M)/(6.9ε) − 1)  ≤  cost  ≤  ln(1/δ)·(10.7·max_M (a_M + b_M)/ε + 1) + 1`.  (The lower bound
> of (c) is the sum over the two macrostates of the larger of the dip and the bump packing — within a factor
> 2 of the display on either side; the sampler of (b) is governed by the worse macrostate.)

### 1.3 Additions of ours (not errors of theirs; all model-relative)

| | statement | label |
|---|---|---|
| A1 | **Finite-depth form of the one-site count.**  If the class contains, with `g₀`, needles at `a` of `L` depths such that no admissible output is valid for two of the `L + 1` instances (prescribed width `w`: minima more than `w` apart), then `P_{g₀}(a` not evaluated`) ≤ δ(L + 1)/L`.  In the ladder model the least expected count at `g₀` over **all** randomised adaptive algorithms is exactly `k(1 − δ(L + 1)/L)` | [P]; exact LP, 22 cases [N] |
| A2 | **Nested sampler with `t_f`.**  `\|E_qW − (β̄ + ρ̄W̄_in)\| ≤ max(h_β, h_{β+ρ}) + ρ̄·h_W` for any three two-sided confidence half-widths of `β̄`, `(β + ρ)‾`, `W̄_in`; with Hoeffding at `δ/3`: `t_f + ρ̄t` | [P]; 168 000 runs [N] |
| A3 | **Allocation beyond first order** (independent sites): the `f ∓ γ` forms of `U`, `L`; the vertex of (c) minimises `U` iff `f_i − γ_i` is largest at the charged site of every `T`; no bound of `U(vertex)` by a multiple of `U(equal)`; `L(λ) ≤ C(m, k)·L(equal)` for every law, level and allocation, sharp for `m = 2` | [P]; 595 random instances (the iff on the 246 with independent sites), closed forms [N] |
| A4 | **The best vertex for `L` is an ordering vertex** (any law, any level); for independent sites and exchangeable constants "most frozen first" is the global minimiser of `L` | [P]; exhaustive on 10 + 40 + 200 instances [N] |
| A5 | **The necessity bound with `ln(1/δ)`.**  Pinsker's bound saturates at `2/KL` as `δ → 0`; the Bretagnolle–Huber inequality gives `N ≥ ln(1/(4δ(1 − δ)))/min KL`, which grows like the sufficient count | [K, search snippet] + [N] |
| A6 | **On the fibre `S` is one interval.**  Along the hidden direction `ν·x*(t) = −Σ_i \|ν_i\|·sign(t − t_i)` is strictly decreasing, so `S` holds between two consecutive zero crossings at most, and a point and its reflection are never both in `S` — without any separation hypothesis.  The other combinatorial claims hold exactly on `{r_i > 3}` | [P]; 60 000 exact draws [N] |

---

## 2. Item 1 — Proposition 11.18e(b′)(i): the randomised count on one site

*Review + replication.  Script `r15_item1_one_site.py`, log `logs/item1_one_site.log`; unisolvence in
`r15_extras.py` (E1), log `logs/extras.log`.*

### 2.1 The lower bound, re-derived [P]

Let the algorithm be a probability law over deterministic adaptive runs; fix `g` and a state `a`.  On the event
`{a` not evaluated on `g}` the run — evaluated states, values seen, output — is identical on
`g_D := g − D·1_a` for every `D`.  If the task is a finite lower bound `ℓ` of the minimum, the output is
invalid on `g_D` once `D > E₀(a) + g(a) − ℓ`; if it is a bracket `[lo, up]` of `ln Z`, once
`D > up + E₀(a) + g(a)` (the report's "once `D` exceeds its upper end" is this, up to the constant).  So the
failure probability on `g_D` is at least `P(a` not evaluated on `g`, threshold `< D)`, which increases to
`P_g(a` not evaluated`)` as `D → ∞` — continuity from below, or a maximum over runs if the algorithm uses
finitely many random bits.  Since every `g_D` is a member, `P_g(a` not evaluated`) ≤ δ`; summing over `a`,
`E|Q(g)| ≥ (1 − δ)|X|`.

Answers to the brief's points.
* **(i) What is assumed about the returned bracket.**  Only that the *expensive* end is finite almost surely
  on the event that `a` is not evaluated (or that a non-finite return counts as a failure): the upper end for
  `ln Z`, the lower bound for the minimum.  Either task.  A lower bound of `ln Z` or an upper bound of the
  minimum costs one evaluation and is not constrained.  **Needles suffice**: the argument uses `g_D ∈ 𝒢` for
  arbitrarily large `D` and nothing else (m3).
* **(ii)** For every `g`, every algorithm (adaptive, randomised); `|Q(g)|` counts *distinct* states; instance by
  instance, not only in the supremum.
* **Why the limit is needed, and what replaces it at a prescribed width (A1).**  With a prescribed width a
  ladder of `L` depths does it: a run that leaves `a` unevaluated on `g₀` is the same on the `L + 1` instances
  that differ at `a` only, and its output is valid for at most one of them, so
  `L·P_{g₀}(a` not evaluated`) ≤ (L + 1)·δ`.

### 2.2 The quantifier "every randomised algorithm", replicated [N, exact]

Linear programme over behavioural strategies (sequence form): values on a ladder `0 > −s > … > −Ls`, task
"minimum within a prescribed width `< s`" (outputs may be taken to be levels), `k = 2, 3, 4` states,
`L = 1, 2, 3, 5` (`k = 4`: `L ≤ 3`), `δ = 0.05, 0.2`; up to 8 952 variables and 256 instances.  Objective: least
`E|Q(g₀)|` at `g₀ = (0, …, 0)` subject to failure `≤ δ` on every instance.  **The LP value equals
`k(1 − δ(L + 1)/L)` in all 22 cases** (e.g. `k = 3, δ = 0.05`: `2.700, 2.775, 2.800, 2.820` for `L = 1, 2, 3, 5`,
against `(1 − δ)k = 2.85`), and is attained by "with probability `δ(L + 1)/L` evaluate nothing and guess a
level".  The limit `D → ∞` of the proposition is this ladder made infinite.

### 2.3 "Attained": the algorithm written out [P; N, exact]

One site, `k` states, weights `z(x) = e^{−E(x)}`.  With probability `1 − kδ` evaluate everything and return the
exact answer; with probability `kδ` draw `a` uniformly, evaluate the other `k − 1` states and return
* minimum: the lower bound `ℓ_a = min_{x≠a} E(x) − w` (`w ≥ 0`); invalid iff `E(a) < min_{x≠a} E(x) − w`;
* `ln Z`: the bracket `[ln Z_a, ln Z_a + W]`, `Z_a = Σ_{x≠a} z(x)`; the lower end is always valid, the upper end
  is invalid iff the weight fraction of `a` exceeds `1 − e^{−W}`.

Failure probability on an instance: `δ·#{a` invalid`}`; expected count `(1 − δ)k`.  Exact arithmetic (integers
and fractions) on grids with ties and needles, `k = 2, 3, 4` (49, 343, 2 401 instances per task):

| task | parameter | worst number of invalid skips, `k = 2 / 3 / 4` | where |
|---|---|---|---|
| minimum | `w = 0, 1/10, 1, 3` | 1 / 1 / 1 | a strict minimiser deeper than `w` |
| `ln Z` | `W = ln 1.05`; `ln(4/3)` | 2 / 3 / 4; 2 / 3 / 3 | equal weights; three equal heavy states |
| `ln Z` | `W = ln 1.5, ln 1.999` | 2 / 2 / 2 | two equal heavy states |
| `ln Z` | `W = ln 2, ln 3, ln 20` | 1 / 1 / 1 | one dominant state |

in agreement with `min(k, ⌈1/(1 − e^{−W})⌉ − 1)` in every cell; a needle instance has exactly one invalid skip
in all cases.  **So the coordinator's first reading is right on all three counts** (`kδ ≤ 1`; `ln 2` for
`ln Z`; any width for the minimum — indeed `w = 0`).  Two complements.  (1) For `k = 2` no *deterministic* rule
for the bracket after a skip with widths `≤ W < ln 2` avoids an instance on which both skips fail **[P]**: with
`x, y` the two log-weights, the diagonal instances `x = y = s` (`ln Z = s + ln 2`) must be covered by the rule
used after skipping one or the other state; the set of `s` covered by one rule forces that rule to start above
`s + ln 2 − W > s`, so all instances `(x, s)` with `x ≪ s` fall to the other rule, whose brackets have width
`≤ W`; hence each of the two sets of `s` has diameter at most `ln 2`, and two such sets do not cover the line.
(2) The **trivial mixture** — with probability `δ` evaluate nothing — attains `(1 − δ)|X|` with failure `≤ δ`
for every width, every `k`, every `δ ≤ 1`; the claim "attained" is therefore unconditional, and the conditions
are conditions on the report's algorithm (whose merit is that it fails only on instances with a dominant
state).

**Harness XI.22(d)** (read, and re-run: survived): `ln Z`; width `Lw = 3.0`; `k = 2, …, 6`; skip probability
`r` uniform in `(0.05, 0.9)` (so `δ = r/k`); two instances per `k` — one needle of depth 40 among `N(0, 1)`
values, and the flat instance.  It does not test the minimum, and at `Lw = 3` the flat instance with `k = 2`
cannot expose the `ln 2` threshold (with `Lw < ln 2` it would: both skips invalid).  Its last check is the
identity `(k − kδ) = (1 − δ)k`.

### 2.4 The last sentence [P; N]

(iv) of the brief: it is a consequence of the *argument* of (i), with one step that the text does not give
(m2).  The step — a function `h_a` of order below `m` with `h_a = 1_a` on the ball — was checked numerically on
ten (grid, order) pairs with alphabets `(2,2,2)` to `(3,2,2,2)` and `m = 2, 3`: balls around three references
each are unisolvent (rank `= N_ball`), the Lagrange functions exist, and `g + t·h_a` agrees with `g` on
`B ∖ {a}` while the minimum follows `t → −∞`.  The same holds for any fixed unisolvent set.  The second half of
the sentence ("cannot hide from a random point, a needle can") is interpretation, and a good one.

---

## 3. Item 2 — Proposition 11.18f: which allocation

*Review + replication.  Script `r15_item2_allocation.py`, log `logs/item2_allocation.log`; `r15_extras.py`
(E2–E4).  Re-run of harness XI.23: survived, with `greedy_gain_upper = 8.066`, `greedy_gain_lower = 13.12`.*

### 3.1 (a) [P; N]

`pen` depends on the changed set only, so `Z(A − pen)/Z(A) − 1 = Σ_S P(S)(e^{pen(S)} − 1)`; for independent
sites and site penalties `E e^{pen} = Π_i(1 − p_i + p_i e^{γ_i})`.  Mean penalty: `E pen = Σ_K g_K·P(K ⊆ S)`
with `g_K` the charge of `K`; for independent sites with a common `p`, `P(K ⊆ S) = p^k`, so
`E pen = p^k Σ_K g_K = p^k Γ` — **exactly, for every `0 ≤ k ≤ m`, arbitrary constants, and every allocation of
level `k`, not only equal shares**.  The route of the report is the counting form
`pen_k(S) = Σ_T c_T C(|T ∩ S|, k)/C(m, k)` with `E C(Bin(m, p), k) = C(m, k)p^k`; all that is used is
`P(K ⊆ S) = p^k` for every `k`-subset.  Checked with equal shares on 40 random instances (`n = 5, 6, 7`, `m = 3, 4`,
every `1 ≤ k ≤ m`; random constants; a common `p`, and unequal `p_i` against `Σ_K g_K Π_{i∈K} p_i`): largest
error `1.5·10⁻¹¹`.  For other allocations the statement is the one line above.

### 3.2 (b) [P; N]

`U` is a log-sum-exp of linear functions of `λ`, hence convex; `L` is minus one, hence concave; the gradients
are the tilted probabilities (30 instances with *non-product* laws, levels 1 and 2: no violation of midpoint
convexity/concavity; finite differences agree to `1.5·10⁻⁹`).

*The "iff", said exactly.*  On the product of simplices `{λ_{T,·} ≥ 0, Σ_K λ_{T,K} = c_T}`, `λ` minimises `U`
iff for every `T` with `c_T > 0` the support of `λ_{T,·}` lies in `argmin_{K ⊆ T} P⁺_λ(K ⊆ S)`, **where
`P⁺_λ ∝ P·e^{pen_λ}` is the tilted law of `λ` itself**.  It is a fixed-point condition, not a recipe; ties are
allowed in the sense that mass may sit on several minimisers, but which splits are optimal is again decided at
`λ`.  Checked: at the numerical minimiser (exponentiated gradient, Frank–Wolfe gap `≤ 4.1·10⁻⁸`) of 25 instances
no constant sits on a subset that is not among the least often changed; none of 500 random allocations
satisfies the condition, and none is below the minimum; on an exchangeable instance all tilted probabilities
coincide at equal shares (levels 1, 2).

*The minimum of `L`.*  (i) **Not every vertex is a local minimum.**  Moving a constant from `K` to `K′` changes
`L` at the rate `P⁻_v(K′ ⊆ S) − P⁻_v(K ⊆ S)` (`P⁻_v ∝ P·e^{−pen_v}`); a vertex is a strict local minimum iff
every constant sits on the strictly least-often-changed subset of its `T` under `P⁻_v`.  Counted on all 59 049
vertices of ten instances (`n = 5`, triples, level 1): `1, 60, 60, 16, 17, 46, 42, 1, 17, 4` strict local
minima — few, but often more than one (with large equal constants `60`, which is the number `5!/2` of
distinct ordering vertices).  (ii) **The best vertex is an ordering vertex (A4) [P].**  `L` depends on `λ` only through the
charges `g`, and is concave in `g`; the achievable charge vectors form
`{g ≥ 0 : Σ_{K∈𝒦} g_K ≤ r(𝒦) for all 𝒦, Σ_K g_K = Γ}` with `r(𝒦) = Σ{c_T : T has a k-subset in 𝒦}` (supply
and demand), the base polytope of a coverage polymatroid, whose vertices are the greedy vectors of the linear
orders — "every constant to the first `k`-subset of its `T` in the order"; a concave function is least at a
vertex.  Exhaustive: 10 of 10 (level 1, product and non-product laws), 40 of 40 (level 2, `n = 4`: 51 of the 81
vertices are ordering vertices).  This reduces the search from `C(m, k)^{#T}` vertices to orders.  (iii)
**Without search?**  For independent sites and exchangeable constants (`r` depends on `|𝒦|` only — all `c_T`
equal on all `m`-subsets), yes: all ordering vertices have the same charge profile `g_1 ≥ g_2 ≥ …`, and since
`ℓ_j − ℓ_i` is nondecreasing whenever `p_j ≥ p_i`, the rearrangement inequality puts the largest charge on the
most frozen site: **"most frozen first" is the global minimiser of `L` [P]** (200 of 200 random instances
against all `n!` orders; in both examples of "Numbers" the vertex of (c) is the best vertex).  In general, no:
with constants in `{0, C}`, `C` large, and independent sites, `L(v) → Σ_{i` charged`} −ln(1 − p_i)`, a
minimum-weight hitting set of the hypergraph of the `T` (vertex cover for `m = 2`) **[P, by this reduction]**;
over the ten instances above (three of them with equal constants) the vertex of (c) was the best vertex in 6
— in 3 of the 7 with random constants — and a strict local minimum in 8.

### 3.3 (c) [P; N]

To first order both ends are `Σ_{T,K} λ_{T,K} P(K ⊆ S)` (ratio to `U`, `L` within `10⁻³` at scale `10⁻⁵`, 20
instances), least at the vertex "least probable sub-pattern".  For independent sites and `k = 1` this is the
most frozen site, and with a **linear order** the formula `γ_i = Γ(R_i) − Γ(R_i ∖ {i})` reproduces it exactly
(error `2.7·10⁻¹⁵`); for pairs the "second difference" of THY-RES-0012 §3.2 does (`5.3·10⁻¹⁵`).  Ties: m4.

### 3.4 "Numbers" recomputed (exact enumeration over the 64 changed sets) [N]

| instance | allocation | ours `(U, L)` | theirs |
|---|---|---|---|
| `p = (.01)⁴, (.3)²`; `c = 0.1` | equal site shares | (0.24010, 0.18911) | (0.240, 0.189) |
| | most frozen site | (0.02977, 0.01441) | (0.030, 0.014) |
| | equal pair shares | (0.01647, 0.01423) | (0.016, 0.014) |
| | envelope | (0.00042, 0.00037) | (0.0004, 0.0004) |
| `p = .05`; `c = 0.5` | equal site shares | (1.16710, 0.24841) | (1.17, 0.248) |
| | most frozen site (vertex) | (2.98716, 0.15910) | (2.99, 0.159) |
| | equal pair shares | (0.04776, 0.01694) | not quoted |
| | envelope | (0.00253, 0.00092) | not quoted |

Ratios `8.07` and `13.12` ("8 times", "13 times").  Two further numbers for the first instance: the least `U`
over all level-1 allocations is `0.02587` (the tied frozen sites share; `L = 0.01577`); the best ordering vertex
for `L` is the vertex of (c).

### 3.5 The coordinator's question: when the constants are not small [P; N]

*The brief asks whether the "most frozen site" vertex can make "the lower end `L`" much worse than equal
shares, and describes the mechanism of the **floor** model ("the floor's measure moves to states with frozen
sites changed").  In the report's notation the floor `m₋ = A − pen` gives the **upper** end `U` of `ln Z` (the
lower end of the free energy), and `L` comes from the ceiling.  Both are answered.*

Independent sites, level 1, `f_i = ln((1 − p_i)/p_i)`, `γ_i` the penalty carried by site `i`.  Then (checked on
every instance below)

    U = Σ_i [ sp(γ_i − f_i) − sp(−f_i) ],        L = Σ_i [ sp(−f_i) − sp(−f_i − γ_i) ],        sp(z) = ln(1 + e^z),

with derivatives `σ(γ_i − f_i)` and `σ(−f_i − γ_i)`: the probability that site `i` is changed under the floor,
respectively the ceiling.  A penalty acts as a field against the cost of changing the site: **the floor sees
`f_i − γ_i`, the ceiling `f_i + γ_i`.**

**Floor end (`U`).**
* *Site by site:* `max(p_iγ_i, γ_i − ln(1/p_i)) ≤ u_i(γ_i) ≤ p_i(e^{γ_i} − 1)`.  First order holds while
  `γ_i ≲ 1`; once `γ_i` exceeds `ln(1/p_i) ≈ f_i` the site is changed under the floor with probability above
  one half and every further nat of penalty costs a nat.
* *Criterion (exact) [P]:* the vertex "most frozen site" minimises `U` over all allocations **iff in every `T`
  the charged site `i` has `f_i − γ_i ≥ f_j − γ_j` for every other `j ∈ T`** — the penalty it carries may exceed
  that of its partners by at most the difference of the free-energy costs.  (KKT for a convex function; tested against
  the numerical minimiser on the 246 random instances with independent sites and level 1 — the condition held
  in 105 of them and failed in 141 — with no violation of the equivalence in either direction.)  The minimiser itself equalises `f − γ` over the
  sites that share constants — a water-filling: in the graded family below at `c = 0.3`, `f − γ = 0.12` at all
  eight sites.
* *Against equal shares [P]:* if at the vertex every charged site is changed under the floor no more often
  than the average site of its `T`, then `U(vertex) ≤ U(equal)`; if
  `Σ_T c_T[p⁺_eq(i(T)) − mean_{j∈T} p⁺_eq(j)] ≥ 0` at equal shares, then `U(vertex) ≥ U(equal)` — in particular
  on every homogeneous instance.  (Both implications, stated with tilted probabilities, were tested on all 595
  random instances — any law, levels 1 and 2; their hypotheses held in 253 and 37 of them; no violation.)  **No bound of `U(vertex)` by a multiple of `U(equal)` exists**: one pair of
  tied sites with `c = 2·ln(1/p)` has `U(vertex) = ln(1 + 1/p − p)` against `U(equal) = 2·ln(2 − p)` — ratios
  `1.9, 3.4, 5.0, 10.0` at `p = 0.1, 0.01, 10⁻³, 10⁻⁶`.

**Ceiling end (`L`).**  `ℓ_i(γ_i) ≤ min(p_iγ_i, −ln(1 − p_i))`: a frozen site can carry any penalty for at most
`−ln(1 − p_i)`.  **For every law, level and allocation, `L(λ) ≤ C(m, k)·L(equal)` [P]**
(`pen_λ ≤ C(m, k)·pen_equal` pointwise, then Jensen for `x ↦ x^{C(m,k)}`); for site shares the factor is `m`.  It
is sharp for `m = 2`: a star of `d` pairs around a centre that is slightly more mobile than its leaves has
`L(vertex)/L(equal) = 1.04, 1.18, 1.895, 1.984` at `d = 4, 40, 10³, 10⁵`.  In 595 random instances
`L(vertex) > L(equal)` never occurred; it cannot occur when in every `T` the most frozen site also has the
largest `f + γ^{equal}` — more generally, is the least often changed site of its `T` under the ceiling measure
of equal shares (a hypothesis that held in 326 of the 595).

**A synthetic family** (eight independent sites, all 56 triples, equal constants `c`; exact):

| ensemble | `c` | `U` equal | `U` vertex | `U` minimum | `L` equal | `L` vertex | largest `γ^{vertex} − f` |
|---|---|---|---|---|---|---|---|
| 4 frozen (0.01) + 4 mobile (0.3) | 0.03 | 0.280 | 0.057 | 0.055 | 0.242 | 0.048 | −0.76 |
| | 0.1 | 1.102 | 0.260 | 0.230 | 0.675 | 0.137 | −0.55 |
| | 0.3 | 4.866 | 3.185 | 1.978 | 1.257 | 0.315 | +1.71 |
| | 1.0 | 33.12 | 36.12 | 32.87 | 1.465 | 0.586 | +16.4 |
| graded 0.01 … 0.4 | 0.1 | 1.196 | 0.344 | 0.344 | 0.739 | 0.151 | −0.41 |
| | 0.3 | 5.370 | 4.073 | 3.457 | 1.389 | 0.298 | +1.71 |
| nearly homogeneous, `p ≈ 0.05` | 0.03 | 0.096 | 0.106 | 0.096 | 0.079 | 0.070 | −2.31 |
| | 0.1 | 0.409 | 0.617 | 0.409 | 0.211 | 0.160 | −0.84 |
| | 0.3 | 2.523 | 6.045 | 2.523 | 0.372 | 0.241 | +3.36 |

and, in closed form, nearly homogeneous ensembles of `n` sites with `c` chosen so that `U(equal)` is `0.2`,
resp. `1.0`: `U(vertex) = 0.28, 0.23, 0.21`, resp. `2.49, 1.78, 1.27`, for `n = 6, 12, 30`.

**Answer.**  *Yes for the end set by the floor* (the report's `U`): where the sites differ by much the vertex
stays better than equal shares until its penalties reach the free-energy costs (then it is far from the
optimum — `3.19` against `1.98` — and soon worse than equal shares, in a regime where every bracket is
useless); where the sites are alike it is worse than equal shares as soon as the constants are not tiny (at
`c = 0.003` in the table's family the two differ by one per cent, in the vertex's favour), by factors up to
`2.5` in the usable range.  *No for the end set by the ceiling* (`L`): at most the factor `m`,
and in practice better.  **A rule that is safe at both ends:** charge the most frozen site of `T` only while
`γ_i ≤ γ_j + f_i − f_j` for its partners, and share beyond — that is the minimiser of `U`, a convex problem in
the site penalties; keep the vertex for the ceiling model (the two models may use different allocations).  For
laws that are not products the same statements hold with the tilted probabilities `P^±_λ(K ⊆ S)` in place of
`σ(±γ_i − f_i)`.

---

## 4. Item 3 — Proposition 11.113a: the nested sampler

*Review + replication.  Script `r15_item3_nested.py` (2 000 repetitions per configuration), log
`logs/item3_nested.log`.  Re-run of harness XXIV.12: survived (3 192 runs, no miss; 1 268 of 1 596 misses
without the free term).*

### 4.1 (a), (b) [P; N]

From `e^{−m₋} ≥ e^{−e₋} ≥ e^{−E} ≥ e^{−e₊} ≥ e^{−m₊}`: the ranges, `W = β + ρW_in`,
`A·E_qβ = Z(e₊) − Z(m₊)`, `A·E_qρ = Z(e₋) − Z(e₊)`, `q·ρ/E_qρ = ` the inner sampler, and
`E_q[ρW_in] = E_qρ·E_in W_in`.  Synthetic boxes (own construction: `n` sites, additive model `A`, random
constants on the `m`-subsets, inner sandwich `A ∓` envelope, outer sandwich `A ∓` equal site shares — product
models with exact partition functions; the member `E = A + env·u`): seven instances with 4 096 or 6 561 states,
outer brackets `0.92` to `2.32` nats, inner `0.011` to `0.74`, `E_qρ` from `0.0070` to `0.317`; members random,
two-level (`u = ±1`), at the floor and at the ceiling of the inner box.  Eleven identities per instance —
including the rejection sampler of Proposition 11.113(b) and the product form of `Z(m_∓)` — hold to
`6.7·10⁻¹⁶`; `ρ = 0` on every state with fewer than `m` changed sites.

### 4.2 (c): the error bound [P]

Three two-sided Hoeffding events at level `δ/3`: `2e^{−2nt²} = δ/3` gives `t = √(ln(6/δ)/(2n))` — **`ln(6/δ)` is
right.**  On them, `|E_qβ − β̄| ≤ t_f` and
`|E_qρ·μ − ρ̄W̄_in| ≤ |E_qρ − ρ̄|·μ + ρ̄·|μ − W̄_in| ≤ t_f + ρ̄t` (`μ = E_in W_in ≤ 1`): the display of (c).

### 4.3 The sampling scheme [P; N]

*Valid:* `N_f` fixed; the evaluated proposals chosen by a rule that looks at the acceptance indicators (and
independent randomness) only.  Proof: conditionally on the acceptance pattern the proposals are independent
and the accepted ones have the law of the inner sampler; the number `n` evaluated is a function of the
pattern; Hoeffding for `W̄_in` holds conditionally with `t(n)`, hence unconditionally; the two free means are
means of `N_f` independent draws; union bound.  This covers (A) an independent stream of `N` accepted draws,
(B) all accepted evaluated — `N` random, about `ρ̄N_f` — and (C) "the first `N` accepted", which is what the
coordinator's `nested_sampler.py` does (`acc[:N]`, with `N_f` fixed — read, not run).  That the evaluated
states are among the proposals used for `β̄`, `ρ̄` is immaterial.  *Not covered:* (D) proposals drawn until `N`
are accepted: the free means are then taken at a stopping time that depends on `ρ(x_i)`; measured relative bias
of `ρ̄`: `+10 %` to `+13 %` at `N = 1`, `+1 %` to `+2.5 %` at `N = 3`, below `0.1 %` at `N = 100`.  No miss occurred
in 12 000 runs of (D) — the bound is conservative — but it is not a theorem there.

Coverage, 2 000 repetitions × 6 configurations × 7 instances × `δ ∈ {0.05, 0.3}` = 168 000 runs (schemes A, B,
C; `N_f` from 40 to 4·10⁶; 300 or 2 000 evaluations; the count-vector simulation cross-checked against literal
streams):

| half-width (units of `A`) | misses at `δ = 0.05` (84 000 runs) | at `δ = 0.3` (84 000 runs) | largest `\|error\|/`half-width |
|---|---|---|---|
| theirs, `2t_f + ρ̄t` | 0 | 0 | 0.961 |
| coordinator's, `t_f(1 + \|W̄_in − ½\| + t) + ρ̄t` | 1 | 7 | 1.116 |
| two-end form, `t_f + ρ̄t` (A2) | 1 | 11 | 1.153 |
| free term dropped, `ρ̄t` | 11 371 | 13 216 | — |
| plain sampler, `√(ln(2/δ)/(2N))` | 0 | 0 | — |

Every configuration is far inside its allowance (`δ·2000` misses); the standard deviation of the estimate
agrees with the delta-method value in every configuration (e.g. `0.00399` against `0.00397`).  With `N_f = 40`,
`N = 2000`, dropping the free term misses in 20 112 of 28 000 runs: **a free term cannot be dropped.**

### 4.4 `t_f` in place of `2t_f` (A2) [P; N]

The error is `f(μ) + ρ̄(μ − W̄_in)` with `f(μ′) = (E_qβ − β̄) + (E_qρ − ρ̄)μ′`, affine on `[0, 1]`; so
`|f(μ)| ≤ max(|f(0)|, |f(1)|) = max(|E_qβ − β̄|, |E_q(β + ρ) − (β̄ + ρ̄)|)`.  Both `β` and `β + ρ` lie in `[0, 1]`
(they estimate `Z(e₊)` and `Z(e₋)`).  With Hoeffding for `β̄`, `(β + ρ)‾` and `W̄_in` at `δ/3` each the half-width
is `A(t_f + ρ̄t)`; the argument is deterministic given the three events, so it holds with any confidence
half-widths (empirical Bernstein included): `max(h_β, h_{β+ρ}) + ρ̄h_W`.  Balance at `N_f = N/ρ²` instead of
`4N/ρ²`.  Example (instance I1, `E_qρ = 0.082`, `N = 300`): at `N_f = 14 665` the three half-widths are `0.0329`,
`0.0220`, `0.0201`; at the member on the floor of the inner box (`W̄_in = 1`) and `N_f = 40`: `0.491`, `0.378`,
`0.247`.

**The coordinator's variant** (`nested_brackets`, docstring): `c = β + ρ/2 ∈ [0, 1]`,
`E_qW = E_qc + E_qρ·(μ − ½)`, same point estimate, error
`(E_qc − c̄) + (E_qρ − ρ̄)(μ − ½) + ρ̄(μ − W̄_in)`, three events `c̄, ρ̄, W̄_in`: the bound
`t_f(1 + |W̄_in − ½| + t) + ρ̄t` follows.  **The proof is right.**  It is never below the two-end form and is
below the report's as soon as `t ≤ ½`.

### 4.5 (d) [P]

* The limit `N_f → ∞` and its constant: m9.
* **Does the lower bound of 11.113(d) apply to the inner box although the algorithm knows the outer models?**
  Yes.  In that argument the algorithm may know everything except the member — here `m_∓`, `e_∓`, even
  `Z(e_∓)`, and it may sample `q` freely; the random member takes the values `e₋`, `e₊`, and an evaluation shows
  one fresh bit whatever else is known.  What the argument needs is the *inner* sampler fine-grained
  (`Σ_x q_in(x)² ≪ ε²/sinh²(Δ_in/2)`).  "In order": the Hoeffding count of (c) exceeds the necessary one by
  `2·ln(6/δ)·e^{Δ_in}/(1 − 2δ)²`, a constant for inner brackets of bounded width (the envelopes quoted are
  `0.0016` to `0.27` nats).
* "About `4/(E_qρ)²` proposals per evaluation": `2t_f = ρ̄t ⟺ N_f = 4N/ρ̄²`; right (and `N/ρ̄²` with A2).
* **Nested against plain at equal `N`:** m10.  Derivation: `2√(ln(6/δ)/(2N_f)) + ρ̄√(ln(6/δ)/(2N)) <
  √(ln(2/δ)/(2N))`.  The criterion agreed with the simulated mean widths in 32 of 32 configurations (four
  instances, `N = 100, 1000`, `N_f` at `0.25, 0.8, 1.25, 4` times the threshold).  For the use the coordinator
  expects — `E_qρ` near one half against the triple sandwich — the report's bound needs `N_f > 28 N`
  (`δ = 0.05`), the two-end form `N_f > 7 N`; if every accepted proposal is evaluated the nested bound is wider
  than the plain one unless `E_qρ < 0.137` (two-end form: `0.316`).

---

## 5. Item 4 — `ratio_expected_queries_ge_mixed` against Corollary 11.114(c), (d)

*Read only for the Lean (statement, proof term, and every lemma the proof term names: `logRatio_dipAlt_gt/lt`,
`logRatio_bumpAlt_lt/gt`, `Zw_restr_*_of_disjoint`, `dipAlt_mem`, `bumpAlt_mem`, `dipAlt_ne`, `bumpAlt_ne`,
`expected_queries_ge_packing`, `prob_query_ne_ge`, `sum_detected_le_card`, `QueryAlgorithm`).  **Nothing was
compiled**: of the imports of `BoxAdditions.lean`, `QueryLowerBound.lean` and its five imports are identical in
our tree (`diff`), but `BoxClass.lean`, `BoxRatio.lean` and `BoxAdditions.lean` do not exist in it, so the
brief's condition for compiling is not met.  Review for (d).*

**The statement.**  Hypotheses: `w ≥ 0`; a point of positive weight in `A` and one in `B`; a finite mixture
`(Ω, P)` of abstract `QueryAlgorithm`s; `hcorr`: on every member of the box the output is within `ε/2` of
`logRatio` with probability at least `1 − δ`; `r` in the box; `D j` pairwise disjoint; `hD`: each `D j` is of
one of four kinds — it avoids `B` and its dip (resp. bump) weight *restricted to `A`* exceeds
`(e^ε − 1)·Z_A(r)` (resp. `(1 − e^{−ε})·Z_A(r)`), or the same with `A` and `B` exchanged.  Conclusion:
`(1 − 2δ)·#{sets} ≤ E|Q(r)|`.  `restr` sets the weight to zero outside the macrostate; `logRatio` is
`ln Z_A − ln Z_B`.

**Where each hypothesis is used.**  `hD j` is split into the four cases, each producing an alternative
(`dipAlt` or `bumpAlt` on `D j`); `hr` puts the alternative in the box; `hw`, the two positive-weight points
and the two halves of `hD` give `|logRatio(alt) − logRatio(r)| > ε` — the "avoids" half makes the other
macrostate's weight unchanged; `hdisj` gives capacity one (a point differs from `r` in at most one
alternative); `hcorr`, `hP`, `hP1` go to `expected_queries_ge_packing` with unit weights.  Every hypothesis is
used; `ε`, `δ` carry no sign hypotheses (the degenerate cases are vacuous or trivial).

**(c) against it.**  Every hypothesis is in the sentence or in the preamble of the corollary ("each of
positive weight"; "(c) asks that the perturbed set avoid the other macrostate").  Nothing more is claimed than
proved.  The theorem is slightly *more* general than the sentence (the sets need only avoid the other
macrostate — weight outside both counts for nothing — and `A`, `B` need not be disjoint).  Two things the
sentence leaves implicit: the evaluations are counted **at `r`, in expectation**; "randomised algorithm" is a
finite mixture of objects of a class larger than decision trees, as everywhere in that library.

**(d).**  *Lower bound:* inside `M`, a greedy packing gives
`k_M ≥ max(⌊a_M/(2(e^ε − 1))⌋, ⌊b_M/(2(1 − e^{−ε}))⌋)` if no single state of `M` is heavy; dip sets and bump
sets inside one macrostate compete for the same states, so the theorem gives the larger of the two there, and
it gives the **sum** `k_A + k_B` over the macrostates — their own example "(1 − 2δ)·10, 40, 200" is `5 + 5`,
`20 + 20`, `100 + 100`.  *Upper bound:* (b) with
`N ≤ ln(1/δ)·max(1, 4·max_M max(a_M/(e^{ε/2} − 1), b_M/(1 − e^{−ε/2}))) + 1`, which needs `U_M, V_M > 0` in both
macrostates (there is no one-sided lemma for ratios in the Lean files; at the floor of a macrostate the
statement is on paper).  With `e^ε − 1 ≤ (e − 1)ε`, `1 − e^{−ε} ≤ ε` and `1 − e^{−ε/2} ≥ 3ε/8` on `ε ≤ 1`, and
`max(x, y) ≥ (x + y)/2`: `k_A + k_B ≥ max_M (a_M + b_M)/(4(e − 1)ε) − 1` and
`N ≤ ln(1/δ)·(4·(8/3)·max_M (a_M + b_M)/ε + 1) + 1` — the two-sided bound of m12.  So: **the step from (c) to (d) is a proof, for `ε ≲ 1`, where no single state is heavy and
`U_M, V_M > 0`; `max` is right as an order statement** (sum and max differ by at most 2, and the upper bound is
governed by the worse macrostate).

*A numerical companion to the reading* (`r15_item4_packing.py`, `logs/item4_packing.log`; own code; **not a
substitute for the kernel**): on 400 random boxes with two macrostates and a rest (200 to 1 200 states;
instances generic, at the floor of `A`, at the ceiling of `B`, at `r = 0`), 3 790 heavy sets of the four kinds
— each with three points outside both macrostates added — change the log-ratio by more than `ε`, and so do 610
sets with *overlapping* macrostates (set avoiding `B`, weight restricted to `A`): the two generalities of the
Lean statement are real.  The 800 greedy packings are never below the two floors where no single state is
heavy; the two-sided bound of m12 holds in every such box (largest `N`/upper bound `0.74`); in 186 boxes both
macrostates contribute sets, so the sum exceeds the max.

---

## 6. Item 5 — the necessity argument of Proposition 11.113(d)

*Review + replication.  Script `r15_item5_necessity.py`, log `logs/item5_necessity.log`.  Re-run of harness
XXIV.11: survived (`worst_fail = 0.00718`, `quarter_fail = 0.1602`, `tv_over_bound = 3.502`,
`nkl_over_tv = 3.4`).*

**(i)** `E_D` takes the values `m₋`, `m₊` pointwise: in the box for every `D`.  `q(D)` has mean `w` and
variance `w(1 − w)·Σ_x q(x)² ≤ w(1 − w)·max_x q(x)` (exact; confirmed by enumeration of all `D` on 10 and 14
states): "fine-grained" alone suffices, by Chebyshev.  Quantitatively: m11(iv).
**(ii)** Under the prior the indicators are independent over states; an evaluation at a new state reveals its
indicator and nothing else (nothing at all where `m₋ = m₊`); the next state is chosen from past bits and
private randomness.  Hence the transcript is a kernel applied to `Bernoulli(w)^N`, whatever the algorithm
knows about `m_∓` and `q`.  **Checked exactly**: 80 random adaptive rules on 5 to 8 states, 3 to 5 evaluations
— the law of the transcript, by enumeration of all `D`, is the product law to `1.1·10⁻¹⁶`.
**(iii)** The reduction: m11(i).  The inference from "on every member" to "on the random member" is an
average; the two priors are compared through the same kernel, so the total variation of the outputs is at most
that of the bits.
**(iv)** Pinsker with the divergence of the `N` bits, `N·KL`: `N ≥ 2(1 − 2δ)²/KL` — factor right; **either
direction of the divergence is admissible**, and `KL(w‖w′)` is the smaller one in rows 2–5 of the table and the
larger one in row 1 (`5.71` against `6.77`: the better bound there uses `KL(w′‖w)`).  `w(1 − w)/(c + w)²` is
largest at `w = c/(1 + 2c)` with value `1/(4c(1 + c)) = sinh²(Δ/2)` (re-derived; confirmed numerically at six
widths).  The approximation: m11(iii) (ratio exact/formula `0.77, 0.99, 1.01, 1.03, 1.05` in the five rows).
**(v)** Truncating at `K` times the expectation: `N_exp ≥ 2(1 − 2δ − 2/K)²/(K·KL)`; `K = 4/(1 − 2δ)` gives the
report's `(1 − 2δ)³/(8·KL)` — right; `K = 6/(1 − 2δ)` gives `4(1 − 2δ)³/(27·KL)`, `18.5 %` more.

**The table, recomputed with our own lines** (`δ = 0.05`):

| `Δ`, `ε` | `w`, `w′` | Pinsker: ours / theirs | `N_TV`: ours / theirs | `N_KL`: ours / theirs |
|---|---|---|---|---|
| 0.0605, 0.01 | 0.4849, 0.8186 | 5.71 / 5.7 | 20 / 20 | 68 / 68 |
| 0.5, 0.03 | 0.3775, 0.4962 | 56.90 / 57 | 189 / 189 | 528 / 528 |
| 1, 0.05 | 0.2689, 0.3584 | 88.97 / 89 | 289 / 289 | 815 / 815 |
| 2, 0.08 | 0.1192, 0.1670 | 180.67 / 181 | 575 / 575 | 1634 / 1634 |
| 3, 0.1 | 0.0474, 0.0695 | 384.00 / 384 | 1209 / 1209 | 3455 / 3455 |

`N_KL` on a grid of 19 999 means gives the same integers as on their grid of 399.  `N_KL` over
`2·ln(2/δ)·sinh²(Δ/2)/ε²`: `1.007` to `1.033`; `N_TV`/Pinsker `≤ 3.502`, `N_KL`/`N_TV ≤ 3.40` ("within a factor
3.5": the first is `3.50`).  Exact failure of the plug-in estimate on two-level members: at most `0.00718` on
their grid `i/60` with `N_KL` evaluations (`0.00731` on `i/600` — the science division's `0.0073`), at least
`0.160` with a quarter.  **All reproduced.**

**One addition (A5).**  Pinsker's bound does not grow as `δ → 0` (it saturates at `2/KL`), so as stated the
necessity is "the order in `Δ` and `ε`", not in `δ`.  The Bretagnolle–Huber inequality,
`TV ≤ √(1 − e^{−KL})` **[K — search snippet only: the statement as given in the summary of a web search that
returned C. Canonne's note arXiv:2202.07198 and the Wikipedia article "Bretagnolle–Huber inequality"; neither
opened]**, gives `N ≥ ln(1/(4δ(1 − δ)))/min KL`, about `ln(1/(4δ))·sinh²(Δ/2)/(2ε²)`: within a factor that tends
to 4 of the sufficient count as `δ → 0`.  The inequality was checked on all binomial pairs of the table **[N]**;
at `(Δ, ε) = (1, 0.05)` and `δ = 0.05, 0.01, 0.001`: Pinsker `89, 105, 109`; this form (in the weaker version
`ln(1/(4δ))/KL`) `88, 177, 303`; `N_TV = 289, 578, 1021`; `N_KL = 815, 1170, 1678`.

---

## 7. Item 6 — the conjecture (b′)(ii): a reading of the outline

*Review of each step; replication of the combinatorial steps in exact arithmetic and a measurement of the
density ratio.  Script `r15_item6_reflection.py`, log `logs/item6_reflection.log`.  Re-run of their
`pairing_check.py`: output identical to their stored `out_pairing_check.txt` (72 000 draws, 41 786 separated,
no violation; `logs/rerun_their_pairing_check.log`).  No attempt was made to finish the proof.*

**The picture that makes the outline transparent [P].**  The instances with a given transcript form a line
`β(t) = β + tν` (with `α` moving accordingly); `β_i(t) = ν_i(t − t_i)`, `t_i = −β_i/ν_i` the zero crossing of
coordinate `i ∈ supp ν`.  The index `k` of the outline is the **nearest crossing** to `t = 0`, and the pairing
is the **reflection `t ↦ 2t_k − t` about it**.  With `r_i = |β_i/ν_i| / |β_k/ν_k| ≥ 1`: `β′_i = β_i(1 ± 2/r_i)`.

| step of the outline | verdict | evidence |
|---|---|---|
| same transcript | exact, always | 60 000 exact draws, no violation |
| "`β′` has the signs of `β` except at `k`" | exact iff no crossing lies between the point and its image; guaranteed for `r_i > 2` | fails in 6 852 of 12 898 draws with `min r ≤ 2`, never above |
| "the map is an involution" | guaranteed for `r_i > 3` (the nearest crossing of the image is again `k`) | fails in 3 056 of 5 743 draws with `2 < min r ≤ 3`, never in 41 359 draws with `min r > 3` |
| "it maps `S` into its complement" | **exact for every `β`, more than claimed (A6)**: `ν·x*(t) = −Σ_i \|ν_i\|·sign(t − t_i)` is strictly decreasing in `t`, so `S` is one interval between consecutive crossings and a reflection about a crossing leaves it | never both in 60 000 draws, in all three classes |
| "prior density up to `1 + o(1)`" | true as the range `Λ → ∞`; see below | measured |
| `P(S) ≤ ½` | `S` depends on the signs only: `P(S)` is the fraction of cube points on a hyperplane, exactly `≤ ½` | largest over 180 random `Q`: `0.5000` |
| `ln Z` against the minimum | exact and trivial: `ln Z = −α + Σ\|β_i\| + Σ ln(1 + e^{−2\|β_i\|})` | checked |

So the all-pairs separation by `10⁴·c_max` used in `pairing_check.py` is much more than needed: **the
combinatorial claims hold exactly on `{r_i > 3` for all `i ≠ k}`** — the smallest scaled magnitude more than
three times below every other.

**The question put to us: the density ratio — on what event, and how small is the exceptional set?**  The
Jacobian is 1 in absolute value; the ratio of prior densities is `Π_{i≠k} 1/|1 ± 2/r_i|` (signs equally likely),
times the indicator that `β′` stays in the support.  It is within `e^{±ε}` of 1 essentially when
`min_{i≠k} r_i ≳ 2/ε`, and the scaled log-magnitudes are nearly independent uniforms on an interval of length
`Λ`, so the exceptional set has prior probability about `1 − (1 − ln(2/ε)/Λ)^d ≈ d·ln(2/ε)/Λ`, `d = |supp ν|`.
Measured (40 sets `Q` × 5 000 draws per cell; `n = 7`, mean `d = 4`):

| `Λ` | 20 | 60 | 200 | 1000 | 5000 |
|---|---|---|---|---|---|
| `P(\|ln ratio\| > 0.01)` (predicted) | 0.636 (0.645) | 0.291 (0.294) | 0.098 (0.099) | 0.020 (0.021) | 0.0039 (0.0042) |
| `P(\|ln ratio\| > 0.1)` (predicted) | 0.429 (0.445) | 0.175 (0.178) | 0.056 (0.057) | 0.011 (0.012) | 0.0023 (0.0023) |
| `P(\|ln ratio\| > 1)` | 0.091 | 0.031 | 0.0087 | 0.0018 | 0.0004 |
| `P(min r ≤ 3)` | 0.193 | 0.069 | 0.021 | 0.0040 | 0.0008 |
| `P(β′` leaves the support`)` | 0.017 | 0.0022 | 0.0002 | `< 10⁻⁵` | `< 10⁻⁵` |

**"`1 + o(1)`" is true, with an exceptional set that shrinks only like `d·ln(1/ε)/Λ`** — like the inverse of
the logarithm of the dynamic range of the prior.  For one per cent accuracy on all but one per cent of the
prior at `n = 7` one needs `Λ` of a few thousand: magnitudes spread over `e^{2000}` and more.  That is
admissible (the class has no bound on the affine part) but should be said, and the cutoffs must be ordered:
width `≪` lower cutoff `≪ e^Λ ×` lower cutoff `≪` spread of the constant.

**Which step is the real gap.**  On the cube at order two, none looks false, and the measure theory looks
routine: (1) the exceptional set enters additively and unconditionally — because the reflection preserves the
transcript and the stopping decision is a function of it,
`P(S ∩ stop) ≤ e^{ε}·P(Sᶜ ∩ stop) + P(exceptional)`, so `P(stop) ≤ (1 + e^{ε})(δ + P(exceptional) + P(lucky))`;
no statement uniform over transcripts is needed.  (We did not compute `P(S | fibre)`; it is the mass of one
interval of the fibre, and a heuristic estimate **[H]** suggests fibre-dependent deviations from the bound `½`
of order `1/ln(`separation/cutoff`)`, so a uniform statement should not be expected.)  (2) "Lucky outputs off `S`": off
`S` the minimum is affine in `t` with slope `ν·(x* − x¹)`, a non-zero even integer for an integer `ν`, so a
bracket of width `w` covers a `t`-window of length at most `w/2` on each interval; its posterior mass is small when the lower cutoff is far above `w` — needs
an estimate integrated over fibres; routine.  (3) `ln Z` against the minimum: exact (above).  **The real gap
is the extension** — order above two, or more than two states — **and there the pairing itself fails, not only
its write-up**: both facts it rests on (the minimiser is the sign pattern of the coefficients; a reflection of
the smallest coefficient flips exactly one coordinate of it) are lost.  One site with three states already
shows it: with `h = α + b₁[x = 1] + b₂[x = 2]`, `|b₁| ≪ |b₂|`, `b₂ < 0`, reflecting `b₁` does not move the
minimiser, so `S` is mapped into `S`.  At order three on the cube the minimiser is a greedy solution of parity
constraints, and the reflected coefficient may be one that the larger ones already determine.  A proof beyond
the cube at order two needs a different involution — presumably a reflection about the nearest crossing of a
coefficient that is *decisive* for the minimiser.

Two remarks on the statement itself.  The outline yields `(1 − 2δ)(n + 1) − o(1)`, not the conjectured
`(1 − δ)`; and the conjectured bound, if true, is attained at every width by the trivial mixture of §2.3
(evaluate nothing with probability `δ`), so its `(1 − δ)` is exactly that saving.

---

## 8. Requests to the theory division (can be sent as they stand)

**R15-T1 (Prop. 11.18e(b′)(i)).**  Replace the "attained" sentence and the last sentence by the texts of m1 and
m2, and the hypothesis by that of m3.  Optionally add the finite-depth form A1 (a ladder of `L` depths gives
`P(a` not evaluated`) ≤ δ(L + 1)/L`; exact in the finite model by linear programming), and extend harness
XI.22(d) by (a) the minimum with slack 0, (b) `ln Z` with a width below `ln 2` on two equal states (failure
`2δ`), (c) the trivial mixture.

**R15-T2 (Prop. 11.18f).**  (a) State the formula of (c) with a linear order (m4) and say what happens at ties.
(b) Add the range of validity of the first-order rule (m5): the forms of `U`, `L` in `f_i ∓ γ_i`, the criterion
"`f_i − γ_i` largest at the charged site of every `T`", the site-wise bounds, and `L(λ) ≤ C(m, k)·L(equal)`.
(c) Say which vertex (m6).  *Validation target:* our table of §3.5 from your own code.  *Question:* is the
ordering-vertex statement (A4) known to you in this form, and do you see the best order for non-exchangeable
constants without search in any case of interest (a chain, a band)?

**R15-T3 (Prop. 11.113a).**  (a) State the sampling scheme in (c) (m7).  (b) Replace `2t_f` by `t_f` — Hoeffding
for `β` and for `β + ρ` (m8) — and `4/(E_qρ)²` by `1/(E_qρ)²`; harness XXIV.12 can assert coverage of the
narrower bracket.  (c) Correct the constant of the limit in (d) (m9) and add the comparison with the plain
sampler (m10).  *Stopping condition:* a counterexample to `t_f + ρ̄t` in your harness, or its adoption.

**R15-T4 (Prop. 11.113(d)).**  Adopt the four precisions of m11; add, if you wish, the bound with `ln(1/δ)`
(A5) — after reading a source for the Bretagnolle–Huber inequality, which we have not opened.

**R15-T5 (Cor. 11.114).**  Adopt the two sentences of m12.  If you want (d) machine-checked at the floor or
ceiling of a macrostate: a one-sided `ratio_detect_ge` in the manner of `detect_ge_at_floor`.

**R15-T6 (the conjecture).**  For the write-up on the cube at order two: use the event `{r_i > 3}` in place of
all-pairs separation; use the monotonicity of `ν·x*` along the fibre (A6) for "`S` into its complement"; state
the exceptional probability `≈ d·ln(2/ε)/Λ` and the order of the cutoffs.  We do not offer to finish it; the
extension beyond the cube at order two needs a new pairing (§7).

---

## 9. How to re-run

From `experiments/science/ws_R15/`, with `export OMP_NUM_THREADS=1` (Python 3.13.18, numpy 2.5.3, scipy
1.18.1); one process at a time; every script prints its peak RSS in its last line.

| command | log (complete; last lines `ALL CHECKS PASSED`, `seconds …`, `peak RSS MB …`) | time, peak RSS |
|---|---|---|
| `python3 r15_item1_one_site.py > logs/item1_one_site.log` | `logs/item1_one_site.log` | 1.7 s, 113 MB |
| `python3 r15_item2_allocation.py > logs/item2_allocation.log` | `logs/item2_allocation.log` | 86 s, 64 MB |
| `python3 r15_item3_nested.py 2000 > logs/item3_nested.log` | `logs/item3_nested.log` | 255 s, 83 MB |
| `python3 r15_item4_packing.py > logs/item4_packing.log` | `logs/item4_packing.log` | 0.5 s, 35 MB |
| `python3 r15_item5_necessity.py > logs/item5_necessity.log` | `logs/item5_necessity.log` | 1.7 s, 97 MB |
| `python3 r15_item6_reflection.py > logs/item6_reflection.log` | `logs/item6_reflection.log` | 9.5 s, 39 MB |
| `python3 r15_extras.py > logs/extras.log` | `logs/extras.log` | 0.4 s, 36 MB |
| `python3 -I -B <EXP>/experiments/falsify_conjectures.py --only "XI.22 Randomised"` (and `"XI.23 Shares"`, `"XXIV.11"`, `"XXIV.12"`) | `logs/rerun_their_harness.log` (last lines `RERUN COMPLETE`, peak RSS of children 89 MB) | under 5 s each |
| `python3 -I -B <EXP>/experiments/coordinator_checks/random_ball/pairing_check.py` (no argument: it then writes no file) | `logs/rerun_their_pairing_check.log` (last lines `RERUN COMPLETE`, `seconds 13.2`, peak RSS of the child 13 MB) | 13 s |

Two logs in `logs/` are **not** cited and are kept only as a record: `item3_nested_smoke.log` (60 repetitions,
an earlier version of the script) and `item2_allocation_try1.log` (an earlier version in which two checks of
mine failed for reasons of mine, §11); `logs/_time_pairing.txt` is a stub left by a failed call of
`/usr/bin/time`, which is not installed.  The re-run of their harness wrote nothing into `<EXP>`.

---

## 10. Not checked

* The theory report outside lines 2440–2770 and 9636–10105; Theorem 11.110 and Proposition 11.113(a)–(c′) were
  read only as far as these statements use them.  Parts (a), (b), (c) of Proposition 11.18e and of harness
  XI.22 were read, not reviewed (they were reviewed in SCI-REV-0013).
* **No Lean was compiled.**  `BoxAdditions.lean`, `BoxRatio.lean` and `BoxClass.lean` were read in full, and
  `QueryLowerBound.lean` from `QueryAlgorithm` to `expected_queries_ge_packing`; `AffineHalf.lean` and
  `ShareLevels.lean` (`cover_of_subset_shares`, on which Proposition 11.18f rests for "every allocation
  covers") were **not opened** — that an allocation covers was only re-derived (for `T ⊆ S` all `k`-subsets
  of `T` lie in `S`, and the other terms are nonnegative) and checked numerically (`r15_extras.py`, E5: 60
  random allocations of levels 1 to 3, every changed set).
* The Maurer–Pontil bound of Proposition 11.113(c′) and the empirical-Bernstein variants of the coordinator's
  script: not checked (A2 applies to them by a deterministic argument; no simulation).
* `nested_sampler.py`: docstring, `nested_brackets` and the sampling lines of `main` read; **not run** (real
  instances are excluded by the brief).
* Item 2: laws that are not products were used in the checks of (b), of A3 (the bound on `L`, the first-order
  comparisons) and A4, but the `f ∓ γ` criterion is stated and tested for independent sites only; level 2
  exhaustively on `n = 4` only; the hitting-set reduction is a paper argument with no computation.
* Item 3: only Hoeffding half-widths; `δ ∈ {0.05, 0.3}`; scheme D measured, not analysed.  The comparison
  with the plain sampler is in units of `Z`, not of `ln Z`.
* Item 5: the lower bound was not simulated against an actual algorithm on a fine-grained instance; the
  `o(1)` terms are argued, not computed.
* Item 6: `P(S | transcript)` was not integrated along fibres; the estimate for lucky outputs is not written;
  nothing beyond the cube at order two was computed except the one-site example.
* Sources: Hoeffding (1963, Theorem 1), Pinsker's inequality, Edmonds' description of the vertices of a base
  polytope, the supply–demand (max-flow) theorem and the rearrangement inequality are used **[K — from memory,
  unverified]**; Bretagnolle–Huber **[K — search snippet]**.  No prior-art search was made for A1–A6; they are
  elementary and nothing is claimed new.

---

## 11. Own errors (found and corrected during the work)

1. **`r15_item3_nested.py`, first smoke run:** `ρ` exceeded 1 by one unit in the last place on the state with
   all sites changed (envelope = site shares there), and numpy's binomial sampler rejected it.  Fixed by
   clipping after a check that the excess is below `10⁻¹²`.  The same run showed that instance I2 had been
   built with penalties larger than the free-energy costs of its sites (outer bracket `10.6` nats); rescaled
   before the run that is cited.
2. **A false alarm of mine:** in the 60-repetition smoke run one error was `3.5` standard deviations out, and
   I suspected the count-vector simulation of scheme C.  A delta-method standard deviation added to the script
   agrees with the simulated one in every configuration of the full run, and a cross-check against literal
   streams passes; the smoke-run value was chance.
3. **`r15_item2_allocation.py`, first run:** two of my own checks failed — the optimiser's stopping tolerance
   (`4·10⁻⁸` reached where I asserted `10⁻⁹`), and a first-order check at a scale (`10⁻³`) that was not small
   enough; in the same version exact ties of the "most frozen site" were decided by rounding in the last bit,
   the count of local minima was taken on a sample with a faulty line, and the random search included the
   trivial level `k = m`.  All corrected before the run that is cited; no number of this report comes from the
   first run.
4. **A conjecture of mine that was false:** I expected `L(vertex) ≤ L(equal)` to hold always for independent
   sites, and tried to prove it; the star of §3.5 refutes it (ratio up to `1.98`).  The provable statement is
   the factor `C(m, k)`.
5. **Arithmetic slip in `NOTES.md`** (step 3): `√(ln(6/δ)/ln(2/δ))` at `δ = 0.5` is `1.339`, not `1.208`; corrected
   in the notes with a correction line; the value is not used in this report.
6. **Item 5 script:** the column printed as "Bretagnolle–Huber" uses the weaker corollary `ln(1/(4δ))/KL`; the
   form `ln(1/(4δ(1 − δ)))/KL` was added after the search, and the script re-run; both are in the cited log.
7. **The two-sided bound for a ratio (m12)** stood in my notes as
   `(1 − 2δ)(max_M(a_M + b_M)/(6.9ε) − 2) ≤ cost ≤ 10.7·ln(1/δ)·max_M(a_M + b_M)/ε + 1`: the `− 2` was needlessly
   weak (it is `− 1`), and the upper bound lacked the `+ ln(1/δ)` of the capped detection probability.  Found
   while writing the numerical companion of §5; the report has the corrected form, which the companion checks.

---

## Coordinator's note (added 2026-11-26, before publication as SCI-REV-0015)

*Read in full by the coordinator.  What was checked of it, and how:*

* **Re-derived by hand** (separate lines, not the report's): the two-end bound A2 /
  m8 (the affine argument); the criterion of m10 and its constants (`κ = 0.855, 0.878,
  0.910`; `5.2 N`; `0.137`; `0.316`); the count `min(k, ⌈1/(1 − e^{−W})⌉ − 1)` of m1 — and,
  before this workstream reported, the `ln 2` threshold itself (SCI-RES-0016 §3, which
  the report confirms); the double charge of m4 (`γ = (1, 1, 1, 1, 0, 0)`, sum 4 against
  `Γ = 2`); the site forms of `U`, `L`, the three site bounds and `L ≤ C(m, k)·L(equal)`
  (A3); the monotonicity argument A6; one row of the necessity table (`Δ = 1`,
  `ε = 0.05`: `w = 0.2689`, `w′ = 0.3584`, `KL = 0.01821`, Pinsker `88.96`).
* **Re-run:** all seven scripts of §9 (`r15_item1` … `r15_item6`, `r15_extras`); each log is
  reproduced line for line apart from its two timing lines (compared by checksum).
* **On real instances**, with the coordinator's own code (`pi_inference/nested_sampler.py`,
  `allocation_core_test.py`; addendum A17 (17)), which this workstream read in part and
  did not run: the two-end bracket A2 was added to `nested_sampler.py` after the
  hand-back: on two enumerated serine instances the truth is inside it in 100 of 100
  repetitions at each of three proposal budgets, and at twenty residues it gives
  `9.4·10⁻⁴` nats where the `2t_f` form gives `1.2·10⁻³` (addendum item 50).  The report's A3 —
  "the minimiser of `U` equalises `f − γ` over the sites that share constants, a
  water-filling" — and the coordinator's closed-form water-filling optimum on the
  enumerated leucine helix (addendum item 54) were found independently on the two
  sides the same morning and say the same thing.
* **The Lean statement** read here without compiling (`BoxAdditions.lean`) is built and
  axiom-checked in the coordinator's replication of the theory division's audit at
  `f7df44f` (`INDEPENDENT_VALIDATION.md` §1.9).
* **Not checked by the coordinator:** the linear programme of §2.2, the exhaustive
  vertex counts of §3.2, the 168 000 coverage runs of §4.3 beyond re-running the
  script, the numerical companion of §5, the density-ratio table of §7, the reading
  of the Lean proof term.
* **One thing the report leaves to the coordinator's side:** its statement (3e) that
  the one-known-mean variant "is never below the two-end form" is about Hoeffding
  half-widths.  With variance-sensitive half-widths the comparison reverses on real
  instances, because `c = β + ρ/2` varies far less than `β` or `β + ρ` (addendum item
  51); the report says in §10 that it did not check those variants.
