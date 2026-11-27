# R4 — Independent review SCI-REV-0003: theory report §11.24, "Rounds of adaptivity: two rounds lie strictly between a fixed sample and full adaptivity"

**Object.**  `docs/THEORY_REPORT.md` §11.24 (lines 5568–5791 at theory commit `5ed4072`): Theorem 11.84,
Lemma 11.85, Theorem 11.86, Corollary 11.87, Proposition 11.88; the workstream report behind it
(`docs/workstreams/U_REPORT.md`); the Lean file `proofs/Frontiers/TwoRounds.lean`; the README
sentence (ix).  **Reviewer.**  Workstream R4 of the science division; first independent referee of
this section.  25 November 2026.  **Everything I computed is in `experiments/science/ws_R4/`**
(`NOTES.md` is the step-by-step log; scripts and outputs are listed in §7).

Labels (COMMON rule 6): **[V]** machine-checked (declaration named), **[P]** paper proof, **[K]**
known and cited, **[N]** numerical, **[C]** conjecture, **[H]** heuristic.  *Review* = I read and
re-derived; *replication* = I re-computed with code written before I opened the authors' code.

---

## 1. Verdicts

**In one paragraph.**  I found **no critical error, one major finding and nine minor ones**; no
exponent, no inequality between exponents and no number of the section changes.  The new mathematics — the
two-round lower bound — is correct: I re-derived the indistinguishability lemma and the whole
proof of Theorem 11.86, the Lean declarations say what the prose says (for two rounds, in
abstract form, with standard axioms only), the twins are members of the class, coincide where
the lemma needs them to, and their gap is what the theorem says; every number of the section
that I re-computed with my own code agrees to the digits printed (`θ₂*(1) = 0.35939a = 1.3683h`,
`T^{(2)}(0) = 0.62432a` at `u = 1`, `h/a = 0.26265`; the exact finite-`n` table in every printed digit).
The batched upper bound (Theorem 11.84) is correct against Algorithm 2L⁺ as written in
`K_REPORT.md` §2.2 on the good event; **but its part (ii), "in every run `|C_l| ≤ …`", is false as
stated** — the cost bound holds on the good event only, because the stopping rule on which
the deterministic count depends is missing from the theory report and misplaced in the
workstream's report (M1; a run with `|C_2| = 393 216 > N_2 = 79 931` is exhibited; repaired by one
line, and no exponent is affected).  The minor findings are mostly about what sentences say
beyond what is proved (§9).  One strengthening, machine-checked in abstract form
(§4.6): the lower bound holds for the **expected** number of evaluations **at one instance**, the
flat histogram of the first block, with no assumption on batch sizes — the two-round analogue
of "at the zero function" in Theorem 11.25(a).

| # | statement of §11.24 | verdict | what I did |
|---|---|---|---|
| 1 | **Theorem 11.84**, Claims A and B (a ladder with `L` rungs is `Σ r_l` rounds) | (i) **proved**; (ii) **false as stated** off the good event, **true with a stopping rule** (M1) — overall "proved with a gap" | review line by line against `K_REPORT.md` §§2.2–2.4; replication of the two claims by an own harness, 350 runs, no violation with valid inner brackets; a violating run without the rule |
| 2 | 11.84: "`k` levels with `L` rungs each need `L^{k−1}` rounds independently of `n`"; "hence `τ^{(r)} → h`" | **proved** given Theorems 11.56, 11.58 and the assembly of `K_REPORT.md` Prop. E; **weaker than one sentence advertises** (m1: `h + η` with `r(η)` rounds, not `h` with finitely many) | review; the assembly for `r ≥ 3` read, not re-derived |
| 3 | 11.84(b): `τ^{(2)} ≤ T^{(2)}(0)`; `0.618, 0.620, 0.624, 0.641, 0.665` | **proved** (with the stopping rule of M1) given Theorem 11.56 and Prop. 11.57 (refereed, R8); golden ratio proved | review; replication of all five values |
| 4 | 11.84(c): values `T^{(r)}(0)/a`, `r ≥ 3`; rate | **numerical** as labelled | replication for `r = 3` only (`≤ 0.5403a`); `r ≥ 4` not re-computed by anyone but the workstream |
| 5 | **Lemma 11.85**, two rounds **[V]** | **proved, machine-checked; label correct** | read the Lean file, elaborated it from source, printed axioms; end-to-end exact test on whole cubes |
| 6 | Lemma 11.85, `r` rounds **[P]** | **proved** (one remark on "batch sizes", m3) | re-derived |
| 7 | **Theorem 11.86** (`τ^{(2)} ≥ θ₂*(u)`; twins) | **proved** | re-derived every step; replication of the twins from the statement at finite `n` |
| 8 | `θ₂*(u) > h` for every `u > 0`; table of `θ₂*/a`, `θ₂*/h`, best `φ₁` | **proved** (inequality); values **replicated** | re-derived (Jensen); own code at `u → 0, 0.1, 0.5, 1, 2, 3, 4, 6, 10` |
| 9 | "Exact sums" table (`n ≤ 3200`, `u = 1, 2`) | **replicated** to all printed digits | own implementation; all structural properties checked, not assumed |
| 10 | **Corollary 11.87** (`a > T^{(2)}(0) ≥ τ^{(2)} ≥ θ₂* > h`) | **proved** given 1–8; "`τ^{(48)} ≤ 0.342a`" numerical, not replicated | review |
| 11 | **Prop. 11.88**(a) conditional covering | **proved**; replicated by exact counting | review + own counting, 7 pairs, `n ≤ 3200` |
| 12 | 11.88(b) shadows | **proved** | re-derived |
| 13 | 11.88(c) radial instances: `τ^{(1)} = a`, `τ^{(2)} = h` | **proved** given Theorem 11.51 (its algorithm is two batches; bounded accuracy read, not re-derived in detail) | review |
| 14 | 11.88(d) block-radial on two known blocks | lower half **proved** (= row 7); upper half **sketch**, as labelled | review of the lower half only |
| 15 | 11.88(e) nested basins; three-block continuation | **not examined**; labelled sketch/numerical | — |
| 16 | README (ix) headline | the inequalities are theorems (paper proofs); the three numbers are evaluations of proved formulas; everything is asymptotic (§8) | — |

---

## 2. The claim examined, with all quantifiers

**Setting [K, §§11.16–11.19].**  `Q_n = {0,1}ⁿ` with Hamming distance `d`; `L_u(Q_n)` = functions `ψ`
with `|ψ(x) − ψ(y)| ≤ u·d(x,y)`; `A(ψ) = 2^{−n}Σ_x e^{−ψ(x)}` (uniform reference measure, no known
part); an algorithm is `(ε/2, δ)`-correct on a class if for **every** member
`P(|output − ln A(ψ)| ≤ ε/2) ≥ 1 − δ`.  ("Accuracy `ε`" in the report is this: tolerance `ε/2`.  Two
instances defeat such an algorithm when their `ln A` differ by more than `ε`, i.e. by more than
twice the tolerance — the "`> 2ε`" of an `(ε, δ)` convention.)  Evaluations are exact.  `p_u = 1/(1+e^u)`,
`Λ₁ = ln(2/(1+e^{−u}))`, `f(ρ) = KL(ρ‖½)`, `k(ρ) = KL(ρ‖p_u) = f(ρ) + uρ − Λ₁`, `a = f(p_u)`, `h = f(Λ₁/u)`.

**What a round is.**  The section says only: "an `r`-round algorithm asks `r` batches of
evaluations, each chosen after the answers to the earlier ones".  The proofs use the following
model, and nothing weaker would be natural:

* a random seed `ω`; batch `B_1 = B_1(ω)`; batch `B_t = B_t(ω; answers to B_1, …, B_{t−1})` — an
  **arbitrary** function of the seed **and** of all earlier values (so the second batch may depend
  on values, on internal randomness, on both); all points of a batch are answered together;
  the output is a function of `ω` and of all answers.  An algorithm may leave a batch empty.
* Lean (`TwoRound`, two rounds, deterministic): `first : Finset X`, `second : (X → ℝ) → Finset X`
  with `second g = second g'` whenever `g = g'` on `first`, `output : (X → ℝ) → ℝ` with
  `output g = output g'` whenever `g = g'` on `first ∪ second g`.  A randomised algorithm is a
  **finite** mixture `(Ω, P)` of such objects.  This is the paper model for `r = 2`.
* **Cost.**  Upper bounds (Theorem 11.84): the total number of evaluations, bounded in **every**
  run.  Lower bounds (Lemma 11.85, Theorem 11.86): for algorithms whose batch sizes are at most
  `M_1, …, M_r` in every run, the inequality `Σ_t M_t p_t ≥ 1 − 2δ`; it bounds the largest batch,
  hence the total.  So it is the total that matters, not a per-round budget.  Expected batch
  sizes are not treated in the theory report (the workstream has a Markov remark); §4.6 below
  closes this.
* `τ^{(r)}` := exponent of the least cost of `r`-round algorithms that are `(ε/2, δ)`-correct on
  `L_u(Q_n)` at a **fixed** `ε > 0` and fixed `δ < ½`, as `n → ∞`.  The limit is not shown to
  exist: "`τ^{(r)} ≤ X`" is a statement about `limsup`, "`τ^{(r)} ≥ X`" about `liminf`
  (`U_REPORT.md` lines 44–45; the theory report does not say it).

**Lemma 11.85 for two rounds, as machine-checked [V: `card_distinguished_le`, `two_round_bound`].**
`X` any type, `S₁, S₂` finite nonempty; residuals `g s₁ s₂`, `g' s₁ s₂ : X → ℝ` in a class `G`;
`v s₁ : X → ℝ`; sets `W₁ s₁ s₂`, `W₂ s₁ s₂ ⊆ X` with `g = g' = v s₁` on `W₁` and `g = g'` on `W₂`;
every `x` lies outside `W₁ s₁ s₂` for at most a fraction `p₁` of the pairs `(s₁, s₂)` and, for
every `s₁`, outside `W₂ s₁ s₂` for at most a fraction `p₂` of the `s₂`; a functional `Φ` with
`|Φ(g s₁ s₂) − Φ(g' s₁ s₂)| > ε` for all `(s₁, s₂)`.  Then every finite mixture of two-round
algorithms that is `(ε/2, δ)`-correct for `Φ` on `G`, with `|first| ≤ M₁` for every `ω` and
`|second f| ≤ M₂` for every `ω` and **every** `f : X → ℝ`, satisfies `1 − 2δ ≤ M₁p₁ + M₂p₂`.

**Theorem 11.86, restated.**  For all `u > 0`, `φ₁ ∈ (0,1)`, `φ₂ = 1 − φ₁`, `θ ∈ (0, φ₂a)` with
`Ξ(θ, φ₁) > 0`, and all `ε₁ < γ(θ, φ₁) := min{Ξ(θ, φ₁), φ₂k(y¹)}` (`φ₂f(y¹) = θ`): there is
`n₀(u, φ₁, θ, ε₁)` such that for all `n ≥ n₀`, all `δ ∈ [0, ½)`, all `ε ∈ (0, ε₁n]` and every
randomised two-round algorithm that is `(ε/2, δ)`-correct on `L_u(Q_n)` — indeed on the `2^{n+1}`
functions `ψ_{D,s}, ψ_{S,s}` alone — with batch sizes at most `M₁, M₂`:
`M₁p₁ + M₂p₂ ≥ 1 − 2δ`, `p₁ ≤ (n+1)²e^{−nθ}`, `p₂ ≤ (n+1)e^{−nθ}`; hence
`max(M₁, M₂) ≥ (1 − 2δ)e^{nθ}/(2(n+1)²)`, and
`τ^{(2)} ≥ θ₂*(u) := sup{θ : ∃φ₁, Ξ(θ, φ₁) > 0, θ < φ₂a} > h`.

The accuracy regime is therefore: **every fixed accuracy** (and extensive accuracies up to
the small rate `γ`); the algorithm class: **randomised, two batches, correct on the whole
class** (worst case over the class), exact evaluations, uniform cube, no known part.

---

## 3. Verification method and evidence inspected

1. Read, in this order: §11.24; §11.16; Theorem 11.25; §§11.18–11.19; `U_REPORT.md` (whole);
   `TwoRounds.lean` (whole); `K_REPORT.md` §§1–3.4 (Algorithm 2L⁺ and the proof of Theorem K1 = 11.56
   in full); `DEAD_ENDS.md` D45, D50; of the referee reports `R7`, `R8` the accounts of what they
   checked (as reproduced in §§11.18–11.19) and, by search, their passages on the good event,
   the abort rule (R7's M1, R8's m1) and the sample sizes — not the two reports in full.
2. Re-derived by hand: Lemma 11.85 (`r = 2` and general `r`), the three properties of the twins,
   the two alternatives in the mass of the type `(p_u, p_u)` and `θ₂* > h` — these before any code;
   then Claims A and B of Theorem 11.84, the round count, the two-round exponent and
   Proposition 11.88(b) — these before I wrote the harness for Theorem 11.84.
3. Own code for every number I report.  **Written before I opened any of the authors' code**
   (`experiments/workstreams/U/`, `experiments/coordinator_checks/rounds_U/`): the exponents, the
   twins on type grids from the statement of the theorem, the twins on whole cubes with the
   end-to-end test of the lemma, the asymptotic formula against exact values.  **Written after**
   I had read the coordinator's `README.md`, `u_check1.py`, `u_check2.py`, its three output files,
   and the first 80 lines of the workstream's `lb2_exact.py` — but without reading the authors'
   scripts for the same purpose (`batched_ladder_sim.py`, `cond_cover.py`, `u_check3.py`,
   `ub_rounds.py`; I have seen two of their output files): the harness for Theorem 11.84 (its
   design — product instances, six outer profiles, simulated oracle, reduced `K`, two
   mutations — follows the *description* in `U_REPORT.md` §1.4; the implementation is mine),
   the conditional covering counts, the three-round value, the tightness and monotonicity
   checks of §4.5.
4. Lean: elaborated `TwoRounds.lean` from source, printed axioms; wrote and checked a
   strengthening (§4.6).
5. Compared my numbers with the coordinator's and the workstream's outputs (§7).

---

## 4. The lower bound (the new mathematics)

### 4.1 The lemma, re-derived [P; for two rounds V]

Fix the coins `ω`.  Let `G₁(d₁)` be the common value of `F` and `F'` on `𝒲₁` at first distance
`d₁` (hypothesis (b)), anything elsewhere.  *Virtual run:* answer batch 1 by `G₁(d(x¹, s¹))`, let
`B̃₂` be the second batch the algorithm then asks, answer it by `F`.  `B₁ = B₁(ω)` is fixed, so for
uniform `s` each of its points has type `(D₁, D₂)`, independent binomials: it leaves `𝒲₁` with
probability `p₁`.  `B̃₂` is a function of `(ω, s¹)`; given `s¹`, `s²` is still uniform, so each
point of `B̃₂` leaves `𝒲₂` with probability at most `p₂`, whatever its distance to `s¹`.  If no
point of `B₁` leaves `𝒲₁` and no point of `B̃₂` leaves `𝒲₂`, the real runs on `ψ_s` and on `ψ'_s`
both coincide with the virtual run (batch 1: `F = F' = G₁` on `𝒲₁`; hence the real second batch
is `B̃₂`; batch 2: `F = F'` on `𝒲₂`).  So the transcripts differ with probability at most
`|B₁|p₁ + |B̃₂|p₂` over `s`; an `(ε/2, δ)`-correct algorithm must return different numbers on
twins whose targets differ by more than `ε` with probability at least `1 − 2δ`.  ∎

Two observations that the section does not make:

* **(O1)** The union bound for the second round is over the **virtual** batch `B̃₂`, i.e. the
  second batch of the algorithm *run on the function `x ↦ G₁(d(x¹, s¹))`*.  In Theorem 11.86
  `G₁ = g₁`, and `ψ⁰_{s¹}(x) := g₁(d(x¹, s¹))` **is a member of `L_u`** — the flat histogram of the
  first block.  So the batch sizes need only be bounded on members of the class, and — more —
  no bound is needed at all if one counts expectations at that instance (§4.6).
* **(O2)** For `r ≥ 3` the virtual run answers batch `t` by `G_t`, a different function for every
  `t`: it is not a run on one function.  "Batch sizes at most `M_t`" must then be read as "on
  every sequence of answers", or the proof needs one more line (on the event that the earlier
  virtual batches stayed inside their sets the virtual batch `t` *is* the real one, and
  `P(|B̃_t| ≤ M_t, some point of B̃_t ∉ 𝒲_t) ≤ M_tp_t` because `|B̃_t|` is a function of `ω, s^{<t}`).
  With either reading the lemma is true.

### 4.2 The twins are in the class and satisfy the hypotheses [P; N-exact at finite `n`]

`P_j = Bin(n_j, ½)`, `c_j = −ln P_j`, `T = nθ`; `W₁ = {c₁(d₁) + c₂(d₂) ≤ T}`, `W₂ = {c₂ ≤ T}` (a central
interval `[lo₂, n₂ − lo₂]`), `V₂ = {d₂ ∈ W₂} ⊇ W₁` (as `c₁ ≥ 0`); `g_j = −`(largest `u`-Lipschitz
minorant of `ln P_j(mode) − ln P_j`); `F_deep(d) = max_{e∈W₁}[g₁(e₁) − u|d₁−e₁| − u|d₂−e₂|]`;
`F_cap = max(F_deep, g₁ + g₂)`; `F_D, F_S = F_cap` on `V₂`, continued in `d₂` at slope `∓u` outside.

* *Membership.*  `ψ_s(x) = F(d(x¹,s¹), d(x²,s²))` is in `L_u(Q_n)` iff `F` changes by at most `u` when
  one argument changes by one (a flip changes exactly one block distance by one, and every such
  step occurs).  `g_j` is `u`-Lipschitz; `F_deep` is a maximum of `u`-Lipschitz functions (for the
  `ℓ¹` metric on the grid, which is the same condition); so is `F_cap`; the continuation has slope
  exactly `u` in `d₂` and is `F_cap(·, b) ∓ u|d₂ − b|` in `d₁`.  ✓
* *Coincidence.*  `F_deep = g₁` on `W₁` (`g₁` does not depend on `d₂` and is `u`-Lipschitz in `d₁`),
  `g₁ + g₂ ≤ g₁`, so `F_D = F_S = F_cap = g₁(d₁)` on `W₁`; `F_D = F_S` on `V₂` by definition.  ✓
* *Probabilities.*  A type outside `W₁` has probability below `e^{−T}` and there are at most
  `(n₁+1)(n₂+1) ≤ (n+1)²` types; the same in one block for `W₂`.  ✓  The counting hypotheses of
  the Lean lemma hold **with equality**: `s ↦ x ⊕ s` is a bijection of the cube, so
  `#{s : type(x; s) ∉ W₁} = 2ⁿp₁` for every `x`, and `#{s² : d(x², s²) ∉ W₂} = 2^{n₂}p₂` for every
  `x` and `s¹`.
* *Numerically* (own code, §7): on every pair I built — the 40 final pairs of the table and of its
  extension to `n = 6400`, and 7 pairs on whole cubes `Q_12 … Q_16` — the largest step of `F_D`, `F_S`, `F_cap` in each argument is
  at most `u` (on the cubes: the largest difference over all edges is exactly `u`), `F_D = F_S = g₁`
  on `W₁`, `F_D = F_S` on `V₂`, `W₁ ⊆ V₂`, every type has mass at most 1 under `F_S`, the
  probability bounds hold, and the twins differ only outside `V₂`.

### 4.3 The gap [P; N-exact at finite `n`]

`A(F_S) ≤ (n₁+1)(n₂+1)`: on `V₂` the mass of a type is `P₁e^{−g₁}·P₂e^{−g₂}·e^{−(F_cap − g₁ − g₂)} ≤ 1`; outside
it is the mass of `(d₁, b)` times `P₂(d₂)e^{−u|d₂−b|}/P₂(b) ≤ 1`.  `A(F_D) ≥` the mass of the one type
`(x₀, y₀) ≈ (p_un₁, p_un₂)`, `y₀ < lo₂` because `θ < φ₂a`.  With rates `z = d₁/n₁`, `y = d₂/n₂`:

    n⁻¹ ln mass_D(p_u, p_u) = −φ₁a − φ₂a + uφ₂(y¹ − p_u) + min{ −F_deep(p_u, y¹)/n ,  φ₁a + φ₂f(y¹) } + o(1).

*Second alternative* (the cap): `φ₂[f(y¹) + uy¹ − a − up_u] = φ₂[k(y¹) − k(p_u)] = φ₂k(y¹)`.
*First alternative:* `−F_deep(p_u, y¹)/n = min_{(z,y)∈W₁}[φ₁m(z) + uφ₁|z − p_u| + uφ₂|y − y¹|]`, `m = f` on
`[p_u, ½]`; the nearest point of the slice of `W₁` at `z` is `ρ^s(z)`, `φ₂f(ρ^s) = θ − φ₁f(z)`; shells
`z < p_u` are dominated by `z = p_u`.  Using `f(z) + uz = Λ₁ + k(z)`, `a + up_u = Λ₁`, `θ = φ₂f(y¹)`:

    first alternative = min_z [ φ₁k(z) + φ₂(uρ^s(z) − Λ₁) ] = Ξ(θ, φ₁)       (c = φ₁f(z)).

So `ln A(F_D) − ln A(F_S) ≥ nγ − O(log n)`, `γ = min{Ξ, φ₂k(y¹)}`: **the claimed exponent is what the
argument yields.**  I checked each line of the workstream's proof (`U_REPORT.md` lines 328–355),
including the three places where an inequality goes the right way only because `f` is
decreasing on `[0, ½]` and `P(d) ≤ e^{−nf(d/n)}`.
*Against exact values* (`asymptotic_check.py`, `u = 1`, `φ₁ = 0.6`): exact
`n⁻¹[ln A(F_D) − ln A(F_S)]` at `n = 800, 3200, 6400` is `0.00208, 0.00162, 0.00166` at `θ = h`
(`γ = 0.00179`), `0.00111, 0.00060, 0.00066` at `1.15h` (`γ = 0.00085`), `0.00067, 0.00023, 0.00023` at
`1.25h` (`γ = 0.00044`), and `0.00007`, `0.00000` at `1.33h`, `1.40h` where `Ξ < 0` (`n = 6400`); the
heaviest type of `F_D` is `(0.269, 0.269) = (p_u, p_u)` in every case with a positive predicted gap.
The differences are of the size `log n/n` (`= 0.0014` at `n = 6400`), as the proof allows.

### 4.4 `θ₂* > h` [P]

`E_θ(c) = φ₁x_na(c/φ₁) + φ₂D((θ−c)/φ₂) = c + u(φ₁z + φ₂ρ^s) − Λ₁`, and `f(φ₁z + φ₂ρ^s) ≤ φ₁f(z) + φ₂f(ρ^s) = θ`
(convexity), so `φ₁z + φ₂ρ^s ≥ f^{−1}(θ)` and `E_θ(c) ≥ c + D(θ)`.  `D(h) = u·(Λ₁/u) − Λ₁ = 0`.  At `c = 0`,
`z = ½ ≠ ρ^s`, so Jensen is strict: `E_h > 0` on a compact interval, `Ξ(h, φ₁) > 0` for every `φ₁`;
`Ξ` is continuous in `θ` and `h < φ₂a` for `φ₁ < 1 − h/a` (possible because `h < a`).  ✓
Numerically `Ξ(h, φ₁) = +0.0020, +0.0064, +0.0113, +0.0152` at `φ₁ = 0.1, 0.3, 0.5, 0.64` (`u = 1`), and
`θ ↦ Ξ(θ, φ₁)` is decreasing on `(0, φ₂a)` on a 60-point grid at every slope tried, so
`θ₂*(φ₁) = min{φ₂a, root of Ξ(·, φ₁)}` and the supremum is where the two meet.

### 4.5 What the pair yields, and that the lemma loses nothing on it [N-exact]

* The gap of the twins is decreasing in the budget (`gap_scan.py`: 57 budgets, `n = 800`), so
  "the largest budget at which the gap exceeds 1" is well defined.
* **The bound of Lemma 11.85 is attained on the twins up to a polynomial factor** by an explicit
  two-round algorithm that knows the two blocks (`tightness.py`): round 1 = uniform points with
  all their neighbours; a point of type `(d₁, d₂)` with `F(d₁, d₂−1) ≠ F(d₁, d₂+1)` reveals `s²` up
  to the antipode; round 2 = the two points at block-2 distance `0` and `n₂`, where the twins
  differ.  The probability of the revealing set `R` is `1.5p₁`, `1.6p₁`, `1.6p₁` at
  `n = 800, 1600, 3200` (`u = 1`) and `3.0p₁` at `u = 2`, `n = 1600`.  So `−n⁻¹ ln p₁` is the two-round
  exponent of telling this pair apart, up to `O(log n/n)`: nothing is lost in the lemma, and a
  better two-round lower bound needs other instances, not a sharper argument.
* On small whole cubes the bound holds against real algorithms and is nearly attained
  (`small_cube.py`, `small_cube_exact_opt.py`): a posterior-greedy two-round distinguisher, exact
  count over **all** `2ⁿ` centres, 144 tests on `Q_12`, `Q_14` (36 of them on a degenerate pair with
  `W₂` = everything, where the twins are identical): largest (fraction distinguished)/(`M₁p₁ + M₂p₂`)
  `= 0.78`, never above 1; the **exact optimum** over two-round algorithms with one point per batch
  (7 configurations): `0.35 … 0.62` of the bound; two rounds beat one blind batch of the same
  total size (e.g. `0.361` against `0.219`).

### 4.6 A strengthening: expected cost, at one instance [abstract form V; application P]

By (O1) the second round is only ever charged on the virtual instance.  Hence:

**Theorem R4.1.**  In the situation of Lemma 11.85 for two rounds (as machine-checked: abstract
hidden parameters, finite mixtures), with **no assumption on batch sizes**: for every randomised
two-round algorithm that is `(ε/2, δ)`-correct on a class containing the twins, whose targets
differ by more than `ε`,

    1 − 2δ  ≤  E|B₁|·p₁  +  E_{ω, s₁}|B₂(v s₁)|·p₂ ,

where `|B₂(v s₁)|` is the size of the second batch **when the algorithm is run on the virtual
residual `v s₁`**, and the second expectation is over the coins and a uniform `s₁`.  In
particular, if `p₁, p₂ ≤ p`, the expected number of evaluations on the instance `v s₁`, averaged
over `s₁`, is at least `(1 − 2δ)/p`.
**[V]**: `card_distinguished_le_sum`, `two_round_expected_bound`, `two_round_expected_cost`, and the
worst-case form with the size of the second batch bounded on the class only,
`two_round_bound_of_class` — `experiments/science/ws_R4/lean/TwoRoundsExpected.lean`, built on
`TwoRounds.lean`; `lake env lean` exit 0; axioms `propext`, `Classical.choice`, `Quot.sound`.

**Corollary R4.2 (Theorem 11.86 at the flat histogram) [P, as Theorem 11.86, with R4.1 in place of
`two_round_bound`].**  Under the hypotheses of Theorem 11.86 every randomised two-round
algorithm that is `(ε/2, δ)`-correct on `L_u(Q_n)` for some `ε ≤ ε₁n` makes, **in expectation, at
least `(1 − 2δ)e^{nθ}/(n+1)²` evaluations on the instance `ψ⁰_{s¹}(x) = g₁(d(x¹, s¹))`** — the flat
histogram of the first `⌊φ₁n⌋` coordinates — on average over its centre, hence at some centre.
So `τ^{(2)} ≥ θ₂*` holds for expected cost, without the Markov step and its constant, and the
hard instance is named: *for two rounds the flat histogram of a block plays the part that
the zero function plays for adaptive algorithms in Theorem 11.25(a).*  (As there, the
instance is trivial with a hint: `A(ψ⁰_{s¹})` does not depend on the centre, so an algorithm
that is told the instance up to its centre needs no evaluation.  The cost is the price of
being correct on the twins.)  Finite `n`: the rows of the
table hold with `E' = −n⁻¹ ln max(p₁, p₂)`, which equals the printed `E` to four digits.  **[Note added at checkpoint 38: too strong at small `n` — it exceeds the printed `E` by at most `6.1·10⁻⁵` (`u = 2`, `n = 200`: `0.1130` against `0.1129`) and by less than `10⁻⁵` from `n = 800` on; found by the theory division (THY-RES-0007 §1.1), confirmed by workstream R9 with this workstream's own code.]**

---

## 5. Do the Lean statements say what the prose says?

`lake env lean proofs/Frontiers/TwoRounds.lean`: exit 0, no message.  Axioms of
`TwoRound.output_eq_of_virtual`, `card_distinguished_le`, `prob_output_ne_ge`, `two_round_bound`,
`two_round_witness`: `propext`, `Classical.choice`, `Quot.sound` (`lean/out_AxiomCheck.txt`).

* **`card_distinguished_le`** — deterministic algorithm `A`; conclusion
  `#{(s₁,s₂) : A.output (g s₁ s₂) ≠ A.output (g' s₁ s₂)} ≤ (|A.first|·p₁ + M₂·p₂)·|S₁||S₂|`, with the
  size hypothesis only at the virtual residuals (`∀ s₁, |A.second (v s₁)| ≤ M₂`).  This is the
  coupling of the paper proof in counting form, about *outputs* (which is what is used).
* **`two_round_bound`** — the statement of §2 above.  It is Lemma 11.85 for `r = 2` with: abstract
  hidden parameters and sets (more general than block-radial functions); `𝒲₁`, `𝒲₂` allowed to
  depend on both parameters; a finite probability space for the coins; worst-case batch sizes,
  the second for all `f : X → ℝ` (more than needed: `two_round_bound_of_class`, §4.6).
* **No vacuity.**  The hypotheses are jointly satisfiable with a non-trivial conclusion:
  `two_round_witness` instantiates them (hidden spike on `N` points) and concludes
  `(1 − 2δ)N ≤ M₁ + M₂`, which is the truth for that problem.  `TwoRound` has no junk fields.
* **What is not machine-checked** (the label in the report says so, correctly): the
  application.  The paper steps between `two_round_bound` and Theorem 11.86 are exactly five —
  (i) `F_D, F_S ∈ L_u`; (ii) the two coincidences; (iii) the two counts (translation invariance);
  (iv) the gap exceeds `ε`; (v) arithmetic from `1 − 2δ ≤ M₁p₁ + M₂p₂` to the exponent.  (i)–(iii)
  and (v) are elementary and I verified them exhaustively at finite `n` (§4.2); (iv) is the real
  paper proof (§4.3), confirmed against exact sums.  I consider the gap convincingly filled.
  For general `r` nothing is formalised; the paper proof is correct (§4.1).
* Minor: a randomised algorithm in general is a probability measure on an uncountable set of
  deterministic two-round algorithms; the Lean statement covers finitely supported ones.  The
  paper proof does not care, and only finitely many behaviours matter on the finitely many
  functions involved, but that reduction is not written anywhere (m8).

---

## 6. The upper bound against the algorithm as written

**Is a round non-adaptive?**  Yes.  *Stage 1* asks the reference point, one point per fibre (the
trivial brackets) and the first inner procedure on the fibres of all `M_max = K2^{m_max}` outer
points.  `M_max` is a constant of the algorithm; the outer points and the randomness of every
potential inner call are drawn in advance; the base bracket (Proposition 11.57(a) =
`K_REPORT.md` Prop. K0) has a sample size fixed by `(d, x, δ')` and is one batch of `2M` uniform
points; no evaluation of stage 1 depends on another.  *Stage `l`*: `C_l` is computed from the
stored brackets of stage `l − 1`; then the `r_l` batches of `I_l` are run in parallel on the fibres
of `C_l`.  The output is a computation on stored brackets.  So `Σ_l r_l` rounds; with one-round
brackets, `L` rounds; `k` levels of `L` rungs, `L^{k−1}` (each rung of a level-`k` ladder uses a
level-`(k−1)` procedure at most).

**Claim A** (on the good event every call `(i, l)` of the sequential algorithm has `i ∈ C_l`).  A
call for `a_i` at level `j`, pass `M ≥ i`, at rung `l − 1`: `U_i > s_j`, `L_i ≤ s_je^{−b}` with the stored
bracket (induction on `l`).  `M ≤ max{K, 2νs_j/(ℓ_je^b)}` in every run, `ℓ_j` the value at the entry of
level `j` — this is exactly what step (e) of §2.2 compares with, and R8 notes that K1(iv) is
deterministic.  `ℓ_j ≥ λ_j`: for `i' < j` with `N_L(i', M') ≥ K`, the counted points have `W > s_{i'}`
(V1), so `p(s_{i'}) ≥ N_L/((1+η)M')` (V3′); level `i'` was left, so `s_{i'}q_{i'} ≤ e^bℓ_j/c_η` (populated:
`q ≤ p̲/c_η`, `ℓ ≥ s e^{−b}p̲`; negligible: `sq ≤ e^bℓ/((1−η)ν₀) ≤ e^bℓ`) and `q_{i'} ≥ p(s_{i'})` (Step 2).  ✓
The additional `(J+1)(m_max+1)` Chernoff events are paid by `L + 3` in `K`.  ✓

**Claim B** (`|C_l| ≤ N_l`).  Stored lower ends are at least `s₀`.  A member `i > K` with witness `j`
has `L_i ≥ U_ie^{−x_{l−1}} > s_je^{−x_{l−1}}` **provided its stored bracket has ratio at most `e^{x_{l−1}}`**;
it is counted in `N_L(i', M*)`; `M* > K` because `K < i ≤ 2νs_j/(λ_je^b)` (the parenthesis "`< K/2`"
in `U_REPORT.md` line 146 is a slip, m7); `M* ≤ 4νs_j/(λ_je^b)`; the definition of `λ_j` as a maximum
of empirical quantities gives `N_L(i', M*) ≤ 4(1+η)c_η^{−1}e^λνe^{x_{l−1}}`.  ✓  `N_l ≤ 3(J+1)cnt(x_{l−1})`.  ✓
The proviso is the subject of finding M1.

**The two-round exponent.**  `L = 2`, `x₁ = ξn_i` (one-round bracket, `e^{n_iθ_na(ξ) + o(n)}`), `x₂ = b = x/2`
(one-round bracket of bounded accuracy, `e^{n_ia + O(√n_i)}`), `M_max = e^{φan + O(√n)}`,
`|C₂| ≤ min(M_max, poly·e^{ξn_i})`: exponent `max{φa + (1−φ)θ_na(ξ), min(φa, (1−φ)ξ) + (1−φ)a}`.  ✓  For
fixed `ξ` the two terms balance at `1 − φ = a/(2a + ξ − θ_na(ξ))` with value `a(a+ξ)/(2a + ξ − θ_na(ξ))`
(and there `φa ≥ (1−φ)ξ`, so the `min` is the second entry); small slopes:
`(1+t²)/(1+2t)`, `t = √(ξ/a)`, minimal where `t² + t = 1`, value `t = (√5−1)/2`.  ✓ **[P]**

**Replication of Claims A and B** (`batched_sim.py`; my own implementation of the outer loop of
2L⁺ from `K_REPORT.md` §2.2 and of B2L⁺ from §11.24, simulated inner oracle with adversarial
`α`, product instances with six kinds of outer profile, `n_o ≤ 11`, the constants of the theorem
except `K ∈ {6, 10, 16}` and `η' ∈ {1, 20, 100}`; the coordinator has no script for this theorem):

| `u` | runs | good event | Claim A violated (good / other runs) | Claim B violated | rungs with `N_l < M_max` | largest ratio `#C_l / N_l` | negligible levels | mutations detected (λ; no factor 2) |
|---|---|---|---|---|---|---|---|---|
| 1 | 150 | 112 | 0 / 0 | 0 | 174 | 0.027 | 283 | 29; 8 |
| 3 | 100 | 76 | 0 / 0 | 0 | 96 | 0.0073 | 486 | 40; 6 |
| 0.5 | 100 | 79 | 0 / 0 | 0 | 69 | 0.017 | 34 | 4; 0 |

In all 350 runs my 2L⁺ closed through the closure test with a valid bracket (on the good
event) of at most the certified width — so the harness is also a third implementation that
agrees with Theorem 11.56.  An observation, not a defect: at these sizes the batched schedule
asks about **150 times more** inner brackets at rungs `≥ 2` than the sequential algorithm
(`2.1·10⁶` against `1.3·10⁴` in the printed runs) — inside the polynomial factor of Claim B, and
invisible in an exponent, but it is what batching costs.

---

## 7. Numerics: what was re-computed, how to re-run

All in `experiments/science/ws_R4/`; Python 3.13, numpy, scipy; fixed seeds; run from that
directory.  Times are wall-clock on the shared machine (load 10–16 on 4 cores).

| script (arguments) → output | what | sizes | time | result |
|---|---|---|---|---|
| `exponents.py 1.0` → `out_exponents_u1.txt`; `exponents.py 0.5 2.0 3.0` → `out_exponents_other.txt`; `exponents.py 0.1 4.0 6.0 10.0` → `out_exponents_extreme.txt` | `a`, `h`, `θ₂*`, best `φ₁`, `T^{(2)}(0)` (2-d grid from the statement **and** balance formula), small-slope limit, `Ξ(h,·) > 0`, monotonicity of `Ξ` | grids 4001 + zooms; 97 + 80 values of `φ₁` | 7.5 min; ≈ 15 min; ≈ 25 min | table below |
| `twins_exact.py 1.0 1.0 400 800`, `… 1600 3200`, `… 6400`, `twins_exact.py 2.0 1.0 200 400 1600` → `out_twins_*.txt` | Theorem 11.86, the twins from the statement, exact sums in log space; 13 structural checks per pair; bound for all algorithms | type grids up to `4161 × 2241`; 5 splits × ≤ 40 bisection steps | 12 s; 3 min; 8 min; 2 min | table below |
| `asymptotic_check.py 1.0 0.6 800 3200 6400` → `out_asymptotic_u1_phi06.txt` | exact gap rate against `γ`; heaviest type of `F_D` | up to `3841 × 2561` | 32 s | §4.3 |
| `gap_scan.py 1.0 800 360` → `out_gap_scan_u1_n800.txt` | monotonicity of the gap in the budget | 57 budgets | 10 s | §4.5 |
| `tightness.py` → `out_tightness.txt` | an explicit two-round algorithm on the twins | `n ≤ 3200` | 20 s | §4.5 |
| `small_cube.py` → `out_small_cube.txt` | twins on whole cubes (edges, enumeration, coincidences, counts); posterior-greedy two-round distinguisher, exact over all centres | 7 cubes `Q_12 … Q_16`; 144 tests | 15 s | §4.2, §4.5 |
| `small_cube_exact_opt.py` → `out_small_cube_exact_opt.txt` | exact optimum over two-round algorithms with one point per batch | 7 cubes | 20 s | §4.5 |
| `batched_sim.py 150 20261125 1.0`, `… 100 7 3.0`, `… 100 11 0.5` → `out_batched_sim_u*.txt` | Theorem 11.84, Claims A and B, two mutations | ≤ `1.5·10⁶` outer points per run | 3–5 min each | §6 |
| `three_rounds.py 1.0` → `out_three_rounds.txt` | ladders `(1,1,1)` and `(1,2)` | `481 × 700²` | < 1 min | `(1,1,1)`: `0.5403a`; `(1,2)`: `0.5454a`; so `T^{(3)}(0) ≤ 0.5403a` (report: `0.541a`) |
| `cond_cover_check.py` → `out_cond_cover.txt` | Proposition 11.88(a) by exact counting | 7 pairs, `n ≤ 3200` | 10 s | dual `≤ H(σ)−H(κ) ≤` primal, converging; e.g. `0.02377 ≤ 0.02407 ≤ 0.02500` |
| `lean/AxiomCheck.lean`, `lean/TwoRoundsExpected.lean` (`lake env lean <path>` from the repository root) → `lean/out_*.txt` | statements and axioms of `TwoRounds.lean`; the strengthening of §4.6 | — | 16 s; 67 s | exit 0, standard axioms |

**Exponents (replication; mine / report).**

| `u` | `→ 0` | `0.5` | `1` | `2` | `3` |
|---|---|---|---|---|---|
| `h/a` | 0.25 | 0.25323 | **0.26265** | 0.29676 | 0.34409 |
| `θ₂*/a` | 0.346035 / 0.346 | 0.34947 / 0.349 | **0.35939** / 0.359 | 0.39408 / 0.394 | 0.43965 / 0.440 |
| `θ₂*/h` | 1.38414 / 1.38 | 1.38006 / 1.38 | **1.36834** / 1.37 | 1.32795 / 1.33 | 1.27770 / 1.28 |
| best `φ₁` | 0.654 / 0.65 | 0.6505 / 0.65 | 0.6406 / 0.64 | 0.6059 / 0.61 | 0.5604 / 0.56 |
| `T^{(2)}(0)/a` | 0.618034 / 0.618 | 0.61964 / 0.620 | **0.62432** / 0.624 | 0.64124 / 0.641 | 0.66462 / 0.665 |

(`u = 1`: `a = 0.11094407`, `h = 0.02913914`, `θ₂* = 0.03987221`, `T^{(2)}(0) = 0.06926491`, attained at
`φ = 0.5555`, `ξ = 0.04488 = 0.4045a`.  Small slopes: `T^{(2)}(0)/a = 0.618034 = (√5−1)/2` at
`√(ξ/a) = 0.61803`.)

*A necessary condition for the pair of theorems* — `h < θ₂* < T^{(2)}(0) < a` at every slope; a
lower bound above the upper bound anywhere would refute one of them.  It holds at all nine
slopes computed (`h/a`, `θ₂*/a`, `T^{(2)}(0)/a`): `u = 0.1`: `0.2501, 0.3462, 0.6181`; `u = 4`:
`0.3967, 0.4878, 0.6904`; `u = 6`: `0.4973, 0.5749, 0.7391`; `u = 10`: `0.6371, 0.6902, 0.8063`
(best `φ₁ = 0.654, 0.512, 0.425, 0.310`; the workstream's `0.488`, `0.575` at `u = 4, 6` reproduced).
The three exponents close up as `u → ∞`, in this order.

**Exact twins, accuracy 1 (replication; mine / report).**  `E = −n⁻¹ ln(p₁ + p₂)` at the largest budget
with gap `> 1`, best of the splits `n₁/n ∈ {0.45, …, 0.65}`; "all" `= n⁻¹ ln(2ⁿ/|B(n, k*)|)`.

| `u`, `n` | best `n₁` | `T/n` | gap | `E` (mine / report) | all algorithms (mine / report) |
|---|---|---|---|---|---|
| 1, 400 | 180 | 0.04434 | 1.148 | 0.03005 / 0.0301 | 0.03477 / 0.0348 |
| 1, 800 | 360 | 0.04216 | 1.035 | 0.03411 / 0.0341 | 0.03234 / 0.0323 |
| 1, 1600 | 800 | 0.03987 | 1.065 | 0.03543 / 0.0354 | 0.03092 / 0.0309 |
| 1, 3200 | 1760 | 0.03928 | 1.001 | 0.03684 / 0.0368 | 0.03011 / 0.0301 |
| 1, 6400 | 3520 | 0.03838 | 1.008 | 0.03705 / — (not in the report's table) | 0.02973 / — |
| 2, 200 | 90 | 0.13748 | 1.017 | 0.11294 / 0.1129 | 0.11164 / 0.1116 |
| 2, 400 | 180 | 0.12916 | 1.105 | 0.11520 / 0.1152 | 0.10441 / 0.1044 |
| 2, 1600 | 880 | 0.12555 | 1.006 | 0.12117 / 0.1212 | 0.09934 / 0.0993 |

After the fact I compared with the coordinator's `out_u_check2.txt`: the same `n₁`, `T/n` and `E` in
every row (two independent implementations of the same statement; its `k*` is mine plus one,
an open-ball convention, with the same bound).  The numbers are double-precision evaluations of
exact sums, not interval arithmetic (the bisection puts the gap just above 1, e.g. `1.0009`,
far more than the rounding error of the sums, but this is **[N]**, not **[V]**).

---

## 8. The README headline: what is theorem and what is numerics

> "two rounds provably do **not** reach the adaptive exponent — at slope 1 their exponent lies
> between `0.359a` and `0.624a`, where a fixed sample costs `a` and full adaptivity `0.263a`."

| part | regime and class | status |
|---|---|---|
| "two rounds do not reach the adaptive exponent" | every fixed accuracy `ε > 0` (and `ε ≤ ε₁n`, `ε₁ < γ`), fixed `δ < ½`, `n → ∞`; randomised two-batch algorithms correct on all of `L_u(Q_n)`, uniform measure, no known part, exact evaluations; `liminf n⁻¹ ln(cost) ≥ θ₂*(u) > h` | **theorem [P]**: abstract lemma **[V]**; application to the twins **[P]**, re-derived here, every finite-`n` property verified by exact computation; `θ₂* > h` **[P]**.  That `h` *is* the adaptive exponent is Theorem 11.58 **[P, refereed R8]**, not re-examined |
| "`0.359a`" | `u = 1` | a **number**: the value of the proved formula `sup{θ : Ξ > 0, θ < φ₂a}`; four independent evaluations agree (workstream, coordinator, A1, here: `0.35939`) |
| "`0.624a`" | `u = 1`; `limsup n⁻¹ ln(cost) ≤ T^{(2)}(0)`, worst case over the class, every run | a **number** (`0.62432`): the value of a formula that is an upper bound by Theorem 11.84 **[P; first refereed here: proved once the stopping rule of M1 is added]** on top of Theorem 11.56 and Prop. 11.57 **[P, refereed R8]** |
| "a fixed sample costs `a`" | Theorems 11.44, 11.45 **[P/V, refereed R5]** | not re-examined |
| "full adaptivity `0.263a`" | `h/a = 0.26265` at `u = 1`, closed form; Theorem 11.58 | not re-examined |
| "their exponent" | — | the limit is not shown to exist (m6) |

Everything is a statement about **exponents**.  The lower bound is explicit
(`(1 − 2δ)e^{nθ}/(2(n+1)²)` for `n ≥ n₀`, with `n₀` not quantified, and exact tables up to
`n = 3200`); the upper bounds carry unquantified `e^{o(n)}` factors and no finite-`n` evaluation
of the two-round algorithm exists.  **Not a theorem and not claimed by the README, but
suggested by §11.24 item 2:** a separation at `n = 3200` (m5).  All of it is model-relative
(COMMON rule 7): exact evaluations of a residual known only to be Hamming–Lipschitz on the
cube, uniform reference measure, worst case over that class; the section makes no physical
claim and the round hierarchy should not be read as one.

---

## 9. Findings

Classification as in the earlier referee reports of the repository (R7, R8): *critical* — a
theorem is false; *major* — a displayed claim is false or unproved as written and other
statements lean on it, or a label claims more than there is; *minor* — everything else.

### Critical
None.

### Major

**M1.  Theorem 11.84(ii) is false as stated: the cost of the batched schedule is bounded on the
good event only.**
*Where:* `THEORY_REPORT.md` lines 5617–5624 ("(ii) in every run `|C_l| ≤ K + (J+1)·max{…}` (*Claim B*,
deterministic), so the cost is at most …"); `U_REPORT.md` lines 107–109 and 138–139.
*What:* Claim B bounds `|C_l|` only if every stored bracket of rung `l − 1` has ratio at most
`e^{x_{l−1}}`.  By the definition of a bracket procedure (§11.18) an inner call may return a wider
bracket with probability `δ'` — for instance its own trivial bracket, after an abort.  Then a
member's lower end need not exceed `s_je^{−x_{l−1}}`, the count fails, and `C_l` can be all of
`C_{l−1}`.  The theory report states (ii) with no stopping rule at all.  The workstream's report
has one ("a stored bracket of rung `l−1` has ratio above `e^{x_{l−1}}` → trivial bracket") and
its Claim B says "otherwise B2L⁺ has stopped", but the rule is listed under *Output*, i.e. after
the evaluations it is meant to prevent.
*Demonstration* (`m1_demo.py` → `out_m1_demo.txt`): the candidate sets computed exactly as in the
theorem, with all rung-1 calls returning the (valid) trivial bracket of the fibre: `|C_2| =
162 178, 413 649, 307 083, 393 216` against `N_2 = 59 059, 105 262, 50 968, 79 931` in four of five
configurations (`n_o = 10, 11`; with honest brackets `|C_2| = 145 … 906`).  The last is `|C_2| = M_max`.
*Why it matters:* "the bound `C` on the number of queries holds always, not only on a good
event" is part of the definition of a bracket procedure, and wherever a batched procedure
serves as an inner procedure — the ladders `(1,2)`, `(2,1)` of the recursion 11.84(a), and all
the many-level schedules behind `τ^{(r)} → h` — the accounting of the next level multiplies by
that bound.  It is the gap that referee R7 classified as major for Theorem 11.52 (its M1:
"the cost bound is proved on the good event only; the definition and the induction need it
always") and that R8 met again in a milder form for Theorem 11.56 (its m1).  The probability
of such a run is at most `δ`; no exponent and none of the two-round statements "with
probability `1 − δ`" is affected.
*Correction (one line):* "before stage `l`: if some stored bracket of rung `l − 1` has ratio above
`e^{x_{l−1}}` — or, simpler and sufficient, if `|C_l| > N_l` — stop and return the trivial bracket
`[s₀, s₀e^{2un}]`".  On the good event the rule never fires (V1), so (i) is unchanged, and (ii)
then holds in every run.  **With this rule Theorem 11.84 is proved.**

### Minor

**m1.  One sentence claims the limit with finitely many rounds.**
*Where:* lines 5625–5627: "Every exponent statement derived from Theorem 11.56 — Proposition
11.57, Theorems 11.54 and 11.58 — therefore holds for an algorithm whose number of rounds is
the product of the ladder lengths of its levels, independently of `n`."
*What:* Theorems 11.54 and 11.58 assert `exp(nθ + o(n))`; their algorithms have a number of
levels that grows as the exponent is approached.  Read literally the sentence says
`τ^{(r)} = h` for some finite `r`, which is open question (1) of the same section.  Proved:
for every `η > 0` there is `r(η) < ∞`, independent of `n`, with `τ^{(r(η))} ≤ h + 3η`.
*Correction:* "… holds, for every fixed choice of the parameters of the levels — hence up to an
arbitrary `η > 0` in the exponent —, for an algorithm whose number of rounds …".

**m2.  The recursion (a) is circular as printed.**
*Where:* lines 5630–5633 ("infimum over `φ`, ladders `ξ_1 > … > ξ_L` and `r_1 + … + r_L ≤ r`").
*What:* with `L = 1` this allows `r_1 = r`, so `T^{(r)}` is defined through itself.  `U_REPORT.md`
line 170 has "with `r_l ≤ r − 1`".  *Correction:* add it.

**m3.  Lemma 11.85: "batch sizes at most `M_t`" is ambiguous for `r ≥ 3`, and stronger than needed
for `r = 2`.**  *Where:* lines 5663–5666; `TwoRounds.lean` line 197 (`hM₂ : ∀ ω f, …`).
*What:* (O1), (O2) of §4.1.  *Correction:* say "in every run, on every sequence of answers", or
add the line of (O2); for two rounds state the bound on the class (`two_round_bound_of_class`)
and the expected form (Theorem R4.1).

**m4.  An unlabelled sketch inside the commentary of Theorem 11.86.**
*Where:* lines 5718–5720: "A third round reads it off: the same instance costs a three-round
algorithm `e^{nh+o(n)}`."
*What:* this is the **[sketch]** of Proposition 11.88(d) (`U_REPORT.md` §5.2(b)), and it is about
algorithms for the class of block-radial functions on two **known** blocks.  For algorithms
correct on `L_u` the best three-round bound is `T^{(3)}(0) = 0.541a`, far above `θ₂*`.
*Correction:* "[sketch] for an algorithm that knows the two blocks (Proposition 11.88(d))".

**m5.  The finite-`n` sentence compares two lower bounds.**
*Where:* lines 5586–5588: "At `n = 3200`, `u = 1` and accuracy 1 two rounds need `e^{0.037n}`
evaluations, against the lower bound `e^{0.030n}` that holds for all algorithms and is attained
in the exponent by adaptive ones."
*What:* true word by word, and it reads as a separation at `n = 3200`.  None is shown: the
repository exhibits no adaptive algorithm that costs less than `e^{0.037n}` at such sizes — the
nested algorithms cost `e^{0.061n}` (two levels) and `e^{0.051n}` (three levels) at `n = 4000`,
accuracy `0.87`, at the flat instance (§11.19 remark (1); R8), plain Monte Carlo more, and the
`o(n)` of Theorem 11.58 is not quantified.  Also "need" means
`(1 − 2δ)×` the largest batch in the worst case (or, by §4.6, the expected cost at the flat
histogram).
*Correction:* "from `n ≈ 800` on (`u = 1`, accuracy 1) the two-round lower bound exceeds the lower
bound for all algorithms (`e^{0.037n}` against `e^{0.030n}` at `n = 3200`); the separation from
adaptive algorithms is asymptotic — at these sizes the known adaptive algorithms cost more
than either."

**m6.  "Their exponent lies between".**  *Where:* README line 323; line 5737.  The limit is not
shown to exist: `liminf ≥ 0.359a`, `limsup ≤ 0.624a`.  One clause.

**m7.  A slip in the proof of Claim B.**  *Where:* `U_REPORT.md` lines 146–147, "(it would force
`i ≤ 2νs_j/(λ_je^b) < K/2`)".  The reason is: a member `i > K` with witness `j` has
`K < i ≤ 2νs_j/(λ_je^b)`, so `min{M_max, 2νs_j/(λ_je^b)} > K` and `M* ≥ 2K`.  The conclusion stands.

**m8.  The machine-checked statement is for finitely supported randomness.**  *Where:*
`TwoRounds.lean` lines 184–198 (`[Fintype Ω]`).  Harmless (the paper proof integrates), but the
index of machine-checked statements should say "finite mixtures".

**m9.  Two numbers rest on one unreplicated grid computation without a stored witness.**
*Where:* line 5737 (`τ^{(48)} ≤ 0.342a < τ^{(2)}`) and the values `r ≥ 4` in 11.84(c).  Labelled
correctly as the workstream's.  That *some* `r₀` has `τ^{(r₀)} < τ^{(2)}` is proved; the value 48 is
**[N]**, and `out/ub_rounds_u1_r64.txt` stores values and one parameter per `r`, not the schedule.
An upper bound should come with its witness (the ladders and round allocations), which can
then be checked in milliseconds.

---

## 10. Originality (one paragraph; the deep search is A1's)

Round hierarchies are a standard genre and the coupling of Lemma 11.85 is the standard
round-elimination device ("give the algorithm the first hidden parameter, charge the second
round on a virtual run").  Closest in kind: Canonne–Gur 2017, an adaptivity hierarchy for
property testing, `k` rounds against `k − 1` with a polynomial-versus-linear gap **[A1: full
text of abstract and introduction; I did not read it]**; Agarwal–Agarwal–Assadi–Khanna 2017,
`log* n` rounds for coin identification **[search snippet]**; depth–width trade-offs in parallel
convex optimisation (Balkanski–Singer, arXiv:1808.03880 **[search snippet]**; Nemirovski 1994,
Bubeck et al. **[from memory — unverified]**) and, for *sampling*, Zhou–Wang–Sugiyama, "The adaptive complexity of parallelized
log-concave sampling", arXiv:2408.13045 (ICLR 2025) and Dogariu, "Sharp lower bounds for parallel
log-concave sampling", arXiv:2611.15849 (11 Nov 2026) **[both: arXiv abstract page, read through
a summarising tool, no verbatim text]** — rounds with polynomially many queries each,
`Θ(log d)` rounds, hard instances with a chain of hidden pieces revealed one per round; and
rounds for partition functions in the *sampling-oracle* model (Guo et al.; Harris et al. 2026)
where one round nearly suffices **[A1: full text / abstract]**.  None of these treats the
estimation of a normalising constant over a Lipschitz class by value queries at exponential
budgets, where the question is the *exponent* at a fixed number of rounds; and the separating
instance here is not a chain of hidden pieces but **dilution** — a non-localised structure that
forces a blind batch to spread —, which D50 and Proposition 11.88(e) say is the opposite of
what the chain constructions would suggest.  I concur with A1's classification "plausibly
original theorem, one step of a hierarchy proved, conditional on Theorem 11.58 for the reading
'does not reach the adaptive exponent'".  "Not found" at the depth of abstracts, by A1 and by
two searches of mine (log in §11); not "new".

---

## 11. Reproduction status, and search log

| item | status |
|---|---|
| `θ₂*/a`, `θ₂*/h`, best `φ₁`, `T^{(2)}(0)/a` at five slopes; small-slope limits | **independently replicated** (own code) |
| exact twins: 7 rows of the table, all structural properties | **independently replicated**; identical to the coordinator's values in every digit |
| asymptotic formula `γ` against exact gaps | **independently replicated** (different sizes and split than the workstream's `diag_lb2.py`) |
| twins on whole cubes; Lemma 11.85 against real algorithms | **independently replicated and extended** (exact over all centres; exact optimum for one point per batch) |
| Claims A, B of Theorem 11.84 | **independently reviewed**; **replicated** with an own implementation whose design follows the workstream's description (the coordinator had no script) |
| `T^{(3)}(0) ≤ 0.541a` | **replicated** (`0.5403a`, ladder `(1,1,1)`) |
| Proposition 11.88(a) exact counts | **replicated** |
| `TwoRounds.lean` | **re-elaborated**; statements read; axioms printed |
| `T^{(r)}(0)`, `r ≥ 4`; `τ^{(48)}`; the rate | **not reproduced** |
| Proposition 11.88(d) upper half, (e); three-block computation | **not examined** |
| Theorems 11.25(a), 11.44, 11.45, 11.51, 11.56, 11.58, Prop. 11.57 | **taken as given** (refereed elsewhere); 11.56 exercised by my harness |

*Search log* (COMMON rule 5).  (1) Web search "adaptive complexity of sampling log-concave lower
bound number of rounds polynomially many queries per round" → Zhou–Wang–Sugiyama
(arXiv:2408.13045), Dogariu (arXiv:2611.15849); for both I fetched the arXiv abstract page through
a tool that returns a summary, not the text.  (2) Web search "rounds of adaptivity lower bound
estimation mean OR sum OR integration hierarchy two rounds …" → Agarwal et al. (COLT 2017),
Canonne–Gur (ECCC 2017/029), Balkanski–Singer (arXiv:1808.03880): titles and snippets only; no
hierarchy for sums or integrals found.  (3) `docs/science/workstreams/A1_REPORT.md` §4.1(e), §4.6
**[full text]** for A1's reading levels.  Everything else in §10 is from memory and marked.

---

## 12. Limitations of this review

* I did not re-derive Theorem 11.56, Proposition 11.57, Theorem 11.58 or Theorem 11.51; the
  upper half of the section is "proved **given** these".  My harness exercises Theorem 11.56 at
  small sizes with a simulated oracle only.
* The assembly of the recursion `T^{(r)}` for `r ≥ 3` (Corollary U1.1) was read against
  `K_REPORT.md` Prop. E, not written out again; the values for `r ≥ 4` were not re-computed.
* The harness for Theorem 11.84: `n_o ≤ 11`, reduced `K`, product instances with a radial outer
  profile, no nested levels, no real inner brackets; `|C_l|` stays below 3 % of `N_l`, so the
  *constant* of Claim B is not tested, only its truth.
* The finite-`n` statements are floating-point evaluations of exact sums, not certified.
* The asymptotic check uses one slope and one split (`u = 1`, `φ₁ = 0.6`), `n ≤ 6400`.
* Prior art: A1's search plus two searches; abstracts and snippets only.
* I did not examine Proposition 11.88(e), the three-block computation of `U_REPORT.md` §2.4, or
  the upper half of 11.88(d).

---

## 13. Recommended corrective action

1. Theorem 11.84: add the stopping rule (M1); reword the sentence on Theorems 11.54 and 11.58
   (m1); add `r_l ≤ r − 1` (m2).
2. Lemma 11.85: fix the meaning of "batch sizes" (m3); add the expected-cost form at the
   flat-histogram instance (Theorem R4.1, Corollary R4.2) to the statement of Theorem 11.86 —
   it removes the need for the Markov remark and names the hard instance.  The Lean file
   `experiments/science/ws_R4/lean/TwoRoundsExpected.lean` can be moved into
   `proofs/Frontiers/` as it stands (it imports `TwoRounds.lean`, four declarations, no new axiom).
3. Label the three-round sentence (m4); reword the `n = 3200` sentence (m5); "liminf/limsup" (m6).
4. `U_REPORT.md`: correct the parenthesis (m7) and move the stopping rule before stage `l`.
5. Index of machine-checked statements: "finite mixtures" (m8).
6. Store a witness for every `T^{(r)}(0)` that is quoted (m9).
7. Status line of §11.24 and of README (ix), once 1–5 are done: "refereed (SCI-REV-0003): no
   critical finding; one major (the cost bound of the batched schedule held on the good event
   only; stopping rule added) and nine minor points, corrected".

---

## 14. What is not settled; next steps; requests

**Unresolved (unchanged by this review).**  (1) Is `τ^{(3)} = h`?  (2) The value of `τ^{(2)}` in
`[θ₂*, T^{(2)}(0)] = [0.359a, 0.624a]` — by §4.5 the lower end cannot be raised with these twins.
(3) Strict monotonicity of `τ^{(r)}`.  (4) New here: is `θ₂*` also the *right* cost at the
flat-histogram instance, i.e. is there a two-round algorithm, correct on `L_u`, that spends
only `e^{nθ₂* + o(n)}` there?  Corollary R4.2 is a lower bound at one instance; the upper bound
`T^{(2)}(0)` is a worst-case bound for one algorithm.

**Three most promising next steps.**
1. *The two-round exponent of the block-radial class on two known blocks.*  §4.5 shows the
   lemma is tight on the twins; the workstream conjectures `max{h, ϑ(φ₁), ϑ(φ₂)}` and has a
   sketch of the upper bound.  Proving it would give a class on which the two-round exponent
   is known exactly and strictly between `h` and `a`.
2. *A two-round algorithm with a non-uniform first batch.*  The lower bound is driven by the
   dilution of a **uniform** blind batch over the shells of a flat histogram; `T^{(2)}(0)` uses a
   uniform outer sample.  Whether a first batch that hedges over block splits and shells
   lowers `0.624a` is a concrete question with a variational answer on the type grid.
3. *A certified finite-`n` separation.*  Corollary R4.2 at `n = 3200` is one interval-arithmetic
   computation away from a rigorous statement (see the request below), and the abstract part
   is already machine-checked.

**Requests to the theory division.**
* T1. Apply the corrections of §13, items 1–5.
* T2. Decide whether Theorem 11.86 should be stated at the flat-histogram instance (Corollary
  R4.2); if so, adopt `TwoRoundsExpected.lean`.
* T3. For general `r`, either machine-check Lemma 11.85 by induction or state it with the
  reading (O2) of §4.1.

**Requests to the engineering division** (specifications).
* E1. *Certified rows of the twins table.*  Motivation: the finite-`n` statements of Theorem 11.86
  are floating-point.  Formulation: for `(u, n, n₁, T) = (1, 800, 360, 33.72)`, `(1, 3200, 1760, 125.68)`,
  `(2, 1600, 880, 200.87)` (just below my bisected budgets `33.7288`, `125.6841`, `200.8750`, at which
  the floating-point gaps are `1.035`, `1.0009`, `1.006`), build the twins from the statement
  (reference implementation: `experiments/science/ws_R4/twins_exact.py`, class `Twins`) in
  interval arithmetic and certify (a) the Lipschitz property, (b) the two coincidences —
  both exact comparisons once `g₁` is represented symbolically —, (c) upper bounds for `p₁`, `p₂`,
  (d) a lower bound for `ln A(F_D)` (a certified partial sum over the types around
  `(p_un₁, p_un₂)` and their mirror images; a single type suffices for the exponent but not for a
  gap of 1) and an upper bound for `ln A(F_S)` with difference `> 1` (lower `T` further if the margin at `n = 3200` is too small:
  the gap is decreasing in `T`, `gap_scan.py`).  Output: the four certified numbers per row.  Validation: agreement with
  `out_twins_*.txt` to 4 digits.  Resources: type grids of at most `1761 × 1441`; minutes.
  Stopping condition: three certified rows, or a row where (d) fails — report it.
* E2. *The cost of the two-round algorithm at finite `n`.*  Motivation: nobody has evaluated
  Corollary U1.2 at finite `n`, and batching multiplies the number of inner calls by about
  `10²` at small sizes (§6).  Formulation: the exact expected cost of B2L⁺ with two rungs and
  the constants of Proposition 11.57(b) at the flat instance and at the flat-histogram
  instance of §4.6, `u = 1`, accuracy 1, `n = 10³ … 6.4·10⁴`, as in `K_REPORT.md` §6.4 for the
  sequential schedule; report `ln(cost)/(na)` against `0.624`, against plain Monte Carlo, and
  against the two-round lower bound `E'`.  Stopping condition: the size at which two rounds
  beat one, or the statement that they do not below `6.4·10⁴`.
