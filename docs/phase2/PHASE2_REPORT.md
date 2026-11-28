# Phase II — what observational information is worth to a certified free energy

*Theoretical Research Division, branch `research/phase2-foundations`, 2026-11-28.  Written under
the research owner's directive "MetricChain Phase II — Foundational Mathematics and General
Information Complexity".  Everything here was produced by an AI session; "refereed" means read by
another AI session.  **No statement has been read by a human expert.**  Status labels as in the
theory report: **[V]** machine-checked in Lean (the statement is exactly the Lean statement),
**[P]** paper proof in this file, **[N]** numerical evidence, **[K]** cited, **[C]** conjecture.*

*Starting point.*  The consolidated archive at `fe9f58c` (read through
`consolidated/00_MASTER_INDEX.md`); the two extensions S1, S2 proposed by an independent
preliminary synthesis (GPT-6.2) and handed to this division to "challenge, verify, strengthen,
generalize and formalize".  Verdict on both, and what is new against the archive: §9.

---

## 0. Results at a glance

Setting (§1): weights `w = e^{−ψ}` on the cube `{0,1}ⁿ`, `ψ` `u`-Lipschitz for the Hamming
distance; target `ln A(w)`, `A(w) = 2^{−n}Σ_x w(x)`; randomised algorithms that evaluate `w` and
are correct to `±ε/2` with probability `1 − δ` on the whole class.  Known (theory report, §2 of the
master index): sampling fixed in advance costs `e^{n·a + o(n)}`, every algorithm needs `e^{n·h − o(n)}`
and adaptive ones reach it; `a = KL(p_u‖½)`, `h = KL(ρ₀‖½)`, `ρ₀ = p_u + a/u`.  **New question:** the
algorithm also receives information about the normalised ensemble `μ_w = wπ/A(w)`.

| | information beside evaluations | effect on the cost `N` (number of evaluations) | status |
|---|---|---|---|
| **A** | means of `M` arbitrary observables `φ_i : X → [−1,1]`, each to absolute tolerance `τ` (answers adversarial inside the tolerance) | at most the factor `L = ⌈2τ^{−2} ln(4M/η)⌉`: `N ≥ (1−η)(1−2δ)·N₀/L` for both lower bounds (`N₀ = 2ⁿ/\|B\|` adaptive, `2ⁿ/\|D\|` non-adaptive).  **Both exponents unchanged iff `ln(1/τ) = o(n)` and `ln ln M = o(n)`** — S1 is correct, and both conditions are necessary (row C) | [P]; cores [V] |
| **A′** | the same, exponentially precise: `τ = e^{−γn}`, `ln ln M ≈ βn`, `λ = 2γ + β` | adaptive exponent `≥ h̄(λ) := KL(ρ₀ − λ/u ‖ ½) − λ = h − (1−ℓ)λ + O(λ²)` whenever `h̄(λ) > γ` (S1's argument gives `h − λ`); `ℓ = u^{−1}ln((1−ρ₀)/ρ₀)` is the Chernoff parameter (`0.4900` at `u = 1`).  Upper bound `(1 − γ/ln 2)h`.  Non-adaptive: `≥ a − λ`, `≤ (1 − γ/ln 2)a` | [P]; gap open |
| **A″** | the same on any vertex-transitive finite metric space and for **any reference measure `π`** (any known part) | `N ≥ (1−η)(1−2δ)/(L·P_hit)`; hidden centres are drawn from the *thermally blurred reference* `q ∝ π ∗ e^{−u d}` — the unique law for which mass-normalised cones add up to a constant.  Exponentially strong for homogeneous references; with a field only around tilted baselines, and then below the dip-packing exponent (§2.4) | [P]; identity [V]; values [N] |
| **B** | **exact** means of any observables whose joint Walsh spectrum has `M` non-zero frequencies | at most the factor `\|C\| < 2(M+1)` (S2 is correct); refined: exponent `≥ h̄(ln M/n)`.  The bound on `\|C\|` is attained (`S = W∖{0}`, `W` a subspace) | [P]; cores [V] |
| **C** | the exact joint law of `b = θn` coordinates (or that law to total-variation `τ ≤ c·εδ`; `M = 2^{2^b}` unions of cells) | **exponent exactly `(1 − θ)h`** (and `(1 − θ)a` non-adaptively) — so `ln ln M = o(n)` cannot be dropped from A | [P] |
| **C′** | every bounded observable to tolerance `τ ≤ c·εδ` | **`O(ln(1/δ)/ln(1/τ))` evaluations** suffice for randomised algorithms; deterministic ones still need `Θ̃(τ·2ⁿ)`.  One exact point probability: one evaluation | [P] |
| **E** | `m = e^{νn}` independent samples of the ensemble | `N ≥ exp(n[h̄(ν) − ν] − o(n))` for `ν < ν*`, `h̄(ν*) = 2ν*`; hence samples plus evaluations cost at least `e^{ν* n}`, `ν* = 0.4024·h` at `u = 1`.  Upper bound: `h` (no better algorithm known) | [P] lower; gap open |

In one sentence: *averaged data with honest error bars are worth a factor `τ^{−2} ln M` and
nothing more — whatever is measured — until either the precision or the logarithm of the number
of observables becomes exponential in the size of the system; and the hiding distribution that
proves it is the reference ensemble blurred at the temperature of the class.*

Machine-checked cores: `proofs/Frontiers/ObservationInvariance.lean` (§10).  Exact small-cube
checks of every identity and inequality used: `experiments/phase2/p2_checks.py`; harness block
XXVIII with mutations (§10).

---

## 1. Setting, models, conventions

**Class.**  `X = {0,1}ⁿ` with the Hamming distance `d`, `π` the uniform measure, `u > 0`.  A
weight `w : X → (0,∞)` is **admissible** if `w(x) ≤ e^{u·d(x,y)} w(y)` for all `x, y` (equivalently
`ψ = −ln w` is `u`-Lipschitz); `𝒲_u` is the set of admissible weights.  It is a convex cone,
invariant under translations `x ↦ x ⊕ c` and coordinate permutations, and closed under pointwise
maxima (Lemma 2.1).  `A(w) = E_π w`, `μ_w = wπ/A(w)`.

**Algorithms** (theory report §11.10).  A deterministic algorithm evaluates `w` at adaptively
chosen points and returns a number; a randomised algorithm is a probability distribution over
deterministic ones (private seed `ω`).  It is **non-adaptive** if the set of evaluation points
depends only on `ω` (and, with an oracle, on the oracle's answers) — not on evaluated values.
It is **`(ε/2, δ)`-correct** if for every `w ∈ 𝒲_u`, *and every admissible behaviour of the oracle*,
its output is within `ε/2` of `ln A(w)` with probability at least `1 − δ`.  `Q` denotes the random
set of evaluated points.

**Observation oracles.**
* **(O1) fixed observables, tolerance `τ`.**  Functions `φ_1, …, φ_M : X → [−1, 1]` are fixed and
  known.  Before any evaluation the algorithm receives numbers `o_1, …, o_M` subject only to
  `|o_i − E_{μ_w}φ_i| ≤ τ`.  Any such vector may be returned (published numbers with error bars).
* **(O2) adaptive statistical queries.**  At any time the algorithm may submit a function
  `φ : X → [−1,1]` — depending on its seed, on earlier answers and on evaluated values — and receives a
  number within `τ` of `E_{μ_w}φ`; at most `q` such queries.
* **(O3) exact.**  `τ = 0`.
* Partition, sampling and full oracles: §§5–8, where they are used.

**Constants.**  `p_u = 1/(1+e^u)`, `a = KL(p_u‖½)`, `ρ₀ = u^{−1}ln(2/(1+e^{−u})) = p_u + a/u`,
`h = KL(ρ₀‖½) = KL(ρ₀‖p_u) = ln 2 − h₂(ρ₀)` (`h₂` the binary entropy in nats), `ℓ = u^{−1}ln((1−ρ₀)/ρ₀) ∈ (0,1)`.
`h` is the Chernoff information between the site laws `Bernoulli(½)` and `Bernoulli(p_u)`, and `ℓ` the
optimal Chernoff parameter (theory report §11.18: `h = max_t J(t)`, attained at `t = L = ℓ`).  At
`u = 1`: `a = 0.110944`, `ρ₀ = 0.379885`, `h = 0.029139`, `ℓ = 0.4900`.

**Dips** (theory report, Theorem 11.25).  For an integer `r ≥ 1` the dip of radius `r` at `c` is
`w_{c,r}(x) = max(1, e^{u(r − d(x,c))})`.  It is admissible, equals `1` off the ball `B(c, r−1)` of
`V(n, r−1) = Σ_{j<r} C(n,j)` points, and its **excess** `e_r(x ⊕ c)`, `e_r(x) = (e^{u(r−|x|)} − 1)₊`, has mass
`m_r = E_π e_r = 2^{−n}Σ_{j<r} C(n,j)(e^{u(r−j)} − 1)`, so `ln A(w_{c,r}) = ln(1 + m_r) =: Δ_{r−1}` in the notation
of Theorem 11.25.  For `r/n → ρ ∈ (p_u, ½)`: `n^{−1}ln m_r → u(ρ − ρ₀)` and `n^{−1}ln(2ⁿ/V(n,r)) → KL(ρ‖½)`.

**What is known without an oracle** ([V] lower bounds; [P], refereed, upper bounds).
(i) *Adaptive* (Theorem 11.25(a), `cube_exact_dip_randomized`): if `ε < Δ_k` then
`E|Q(1)| ≥ (1−2δ)2ⁿ/V(n,k)` at the constant weight; for bounded `ε` the exponent is `h`, and nested
adaptive algorithms reach `e^{nh + o(n)}` (Theorems 11.54, 11.58).
(ii) *Non-adaptive* (Theorem 11.45, `nonadaptive_expected_queries_ge`): for two admissible weights
`w₀, w₁` with `|ln A(w₁) − ln A(w₀)| > ε` that differ only on a set `D`, `E|Q| ≥ (1−2δ)2ⁿ/|D|` (translate the
pair by a uniform shift); with the cone `e^{−u|x|}` and the cone flattened at its typical shell the
exponent is `a`, and plain Monte Carlo reaches it (Theorem 11.44).

---

## 2. Theorem A: noisy means of arbitrary observables (the proposed theorem S1)

### 2.1 Four lemmas

**Lemma 2.1 (the cone) [V] (`LogLip.comp_isometry`, `LogLip.convex_comb`, `LogLip.max`, `LogLip.sup'`,
`LogLip.cone`, `LogLip.dip`).**  `𝒲_u` is invariant under every map that preserves `d`, convex, and
closed under finite maxima; `H e^{−u d(·,c)}` and `max(1, H e^{−u d(·,c)})` are admissible for `H > 0`.

**Lemma 2.2 (averaging) [V] (`massOf_convex_comb_eq`, `ensOf_convex_comb`, `massOf_comp_equiv`,
`ensOf_comp_equiv`, `sum_translates_eq`).**  Let `w ∈ 𝒲_u`, `c_1, …, c_L ∈ X`, `λ` a probability vector,
`w̄ = Σ_j λ_j w(· ⊕ c_j)`.  Then `w̄ ∈ 𝒲_u`, `A(w̄) = A(w)`, and `μ_{w̄} = Σ_j λ_j μ_{w(·⊕c_j)}`; for every `φ`,
`E_{μ_{w(·⊕c)}}φ = E_{μ_w}φ(· ⊕ c)`; and `2^{−n}Σ_c w(x ⊕ c) = A(w)` for every `x`, so that for a uniform `c`

    E_c [ E_{μ_{w(·⊕c)}} φ ]  =  E_π φ      for every φ.                                    (2.1)

**Lemma 2.3 (tolerant indistinguishability) [V] (`tolerant_oracle_packing`,
`tolerant_oracle_packing_nonadaptive`).**  Let an oracle be described by a relation "the answer `o`
is admissible for the instance `g`", and let an algorithm be `(ε/2, δ)`-correct for every instance and
every admissible answer.  Let `o₀` be admissible for the baseline `g₀`.  Let `(alt_j)` be
alternatives with weights `wgt_j ≥ 0` such that every point lies in difference sets `{alt_j ≠ g₀}` of
total weight at most `B`, and call `j` **good** if `alt_j` is in the class, `o₀` is admissible for it as
well, and its target differs from that of `g₀` by more than `ε`.  Then

    (1 − 2δ) · Σ_{j good} wgt_j  ≤  E|Q(g₀; o₀)| · B .

The same holds for non-adaptive algorithms and pairs `(g_j, g′_j)`, a pair being good if `o₀` is
admissible for both members.  (For a functional oracle this is the science division's Lemma 1,
`lemma1a`, `lemma1b`; the proof is the same reduction to the packing bound without an oracle,
applied to the instances for which `o₀` is admissible.)

**Lemma 2.4 (Hoeffding for independent translations) [K; the form used: V] (`hoeffding_iid_mean`).**
Let `Y_1, …, Y_L` be independent with values in an interval of length `ℓ_Y` and common mean `m`.  Then
`P(|L^{−1}Σ_j Y_j − m| ≥ t) ≤ 2 exp(−2Lt²/ℓ_Y²)`.

### 2.2 The theorem on the uniform cube

**Theorem A [P; the cores Lemmas 2.1–2.4 are V].**  Let `M ≥ 1`, `0 < τ ≤ 1`, `0 < η < 1`.
(a) *Adaptive algorithms.*  Let `L ≥ 2τ^{−2}(1 − e^{−Δ_k})² ln(2M/η)` be an integer and `ε < Δ_k`.  Every
randomised algorithm that is `(ε/2, δ)`-correct with an oracle (O1) makes, at the constant weight
and with the oracle's answers `o_i = E_π φ_i`,

    E|Q|  ≥  (1 − η)(1 − 2δ) · 2ⁿ / ( L · V(n,k) )

evaluations in expectation.  With an oracle (O2) the same holds with `M` replaced by the number
`q` of statistical queries.
(b) *Non-adaptive algorithms.*  Let `L ≥ 2τ^{−2} ln(4M/η)` and let `w₀, w₁ ∈ 𝒲_u` differ only on a set
`D`, with `|ln A(w₁) − ln A(w₀)| > ε`.  Every non-adaptive `(ε/2, δ)`-correct algorithm with an oracle (O1)
makes, when the oracle answers `o_i = E_π φ_i`, at least `(1 − η)(1 − 2δ)·2ⁿ/(L·|D|)` evaluations in
expectation.
(c) *Exponents.*  If `ln(1/τ) = o(n)` and `ln ln(M + 2) = o(n)`, then for every bounded accuracy both
leading exponents are those without an oracle: `a` for non-adaptive and `h` for adaptive algorithms
(lower bounds from (a), (b) with the instances of §1; upper bounds by ignoring the oracle).  For
`τ = e^{−γn}` and `ln ln M ≤ βn + o(n)` the exponents are at least `h − 2γ − β` and `a − 2γ − β`.

*Proof.*  (a) Let `w = w_{0,k+1}` be the dip with `ln A(w) = Δ_k > ε`, and for `c = (c_1, …, c_L) ∈ X^L` put
`w^c = L^{−1}Σ_j w(· ⊕ c_j)`.  By Lemmas 2.1, 2.2: `w^c ∈ 𝒲_u`, `A(w^c) = A(w)`, `w^c = 1` off
`D_c = ∪_j B(c_j, k)`, and `E_{μ_{w^c}}φ = L^{−1}Σ_j Y_j(φ)` with `Y_j(φ) = E_{μ_w}φ(· ⊕ c_j)`.  Since `w ≥ 1`,
`μ_w = A^{−1}π + (1 − A^{−1})ν` for a probability measure `ν`, so `Y_j(φ)` lies in an interval of length
`2(1 − e^{−Δ_k})`.  Let the `c_j` be independent and uniform.  By (2.1) `E Y_j(φ) = E_πφ`, so by Lemma 2.4
and a union bound the event

    G = { c :  |E_{μ_{w^c}}φ_i − E_πφ_i| ≤ τ  for i = 1, …, M }

has probability at least `1 − 2M exp(−Lτ²/(2(1 − e^{−Δ_k})²)) ≥ 1 − η`.  For `c ∈ G` the answer
`o₀ = (E_πφ_i)_i` is admissible for `w^c`, as it is for the constant weight.  Apply Lemma 2.3 with
baseline `1`, alternatives `w^c` and weights `P(c)`: the good alternatives have weight at least
`1 − η`; a fixed point `x` lies in `D_c` with probability at most `L·V(n,k)/2ⁿ` (union over `j`; each
`c_j` is uniform).  Hence `(1 − 2δ)(1 − η) ≤ E|Q|·L·V(n,k)/2ⁿ`.

For (O2): fix the seed `ω`.  In the run at the constant weight in which every statistical query is
answered by the uniform mean, the queried functions `φ_1^ω, …, φ_q^ω` are determined by `ω` alone.
The run at `w^c` in which the oracle gives the same answers coincides with it as long as no
evaluation falls in `D_c`; these answers are admissible if `c ∈ G_ω` (the event `G` for `φ_i^ω`), and
`P_c(G_ω) ≥ 1 − η` for every `ω`.  The two outputs cannot both be correct, so for every `c`
`P_ω(c ∈ G_ω, Q_ω ∩ D_c = ∅) ≤ 2δ`; integrating over `c`,
`1 − η ≤ P(c ∈ G_ω) ≤ 2δ + P(Q_ω ∩ D_c ≠ ∅) ≤ 2δ + E|Q|·L·V(n,k)/2ⁿ`, which gives
`E|Q| ≥ (1 − η − 2δ)2ⁿ/(L·V(n,k))` (the form `(1−η)(1−2δ)` needs the fixed observables of (O1)).

(b) Put `w_i^c = L^{−1}Σ_j w_i(· ⊕ c_j)`, `i = 0, 1`.  Both are admissible, `A(w_i^c) = A(w_i)`, and they
differ only on `∪_j (D ⊕ c_j)`.  Lemma 2.4 with intervals of length `2` and a union bound over `2M`
events: with probability at least `1 − 4M e^{−Lτ²/2} ≥ 1 − η` the answer `(E_πφ_i)_i` is admissible for
both `w_0^c` and `w_1^c`.  The evaluation points of a non-adaptive algorithm that receives this
answer depend on the seed only; Lemma 2.3 (pairs) with `B = L|D|/2ⁿ` gives the bound.

(c) `n^{−1}ln L = 2n^{−1}ln(1/τ) + n^{−1}ln ln(4M/η) + o(1)`.  ∎

*Remarks.*  (1) **Quantifiers.**  The observables are fixed before the instance is drawn; the
randomness of the translations belongs to the adversary; correctness is required for every fixed
instance and every admissible answer, and is used at the constant weight (with the exact uniform
answer) and at each `w^c`, `c ∈ G` (with the same answer).  The bound is on the expected number of
evaluations *at the constant weight with truthful uniform answers* — the most favourable-looking
situation — hence also on the worst case.  (2) **Constants.**  For the adaptive bound the factor
`(1 − e^{−Δ_k})²` makes `L` small when the accuracy is small; `L = ⌈2τ^{−2}ln(2M/η)⌉` always suffices.
(3) **Unbounded observables.**  If only `Var_c(Y(φ_i)) ≤ σ²` is known, Chebyshev's inequality gives the
same statement with `L ≥ Mσ²/(ητ²)`.

### 2.3 Narrow dips: the exponentially precise regime

Theorem A spends the factor `L` on `L` translates of *one* dip, each of which could have been
hidden alone.  `L` narrower dips, each carrying the `L`-th part of the excess, occupy less space:
a dip with excess `m_r ≈ m_{r*}/L` has radius `r ≈ r* − u^{−1}ln L` and volume `≈ V(n, r*)·L^{−ℓ}`.

**Lemma 2.5 (maxima of dips) [P; (i) V; (ii), (iii) checked exactly on small cubes].**  For
`c = (c_1, …, c_L)` put `w_c = 1 + max_j e_r(· ⊕ c_j)`.  (i) `w_c ∈ 𝒲_u`, and `w_c = 1` off `∪_j B(c_j, r−1)`.
(ii) `L m_r − O_c ≤ A(w_c) − 1 ≤ L m_r` with `O_c = Σ_{j<j′} E_π min(e_r(·⊕c_j), e_r(·⊕c_{j′}))`, and for
independent uniform centres `E O_c ≤ C(L,2)·m_r·V(n,r−1)/2ⁿ`.  (iii) With the probability measure
`μ̃_c = (π + Σ_j e_r(·⊕c_j)π)/(1 + L m_r)`: `TV(μ_{w_c}, μ̃_c) ≤ O_c/(1 + L m_r − O_c)`.

*Proof.*  (i) `w_c` is the maximum of the dips `w_{c_j, r}`.  (ii) For nonnegative numbers
`Σ_j a_j − Σ_{j<j′} min(a_j, a_{j′}) ≤ max_j a_j ≤ Σ_j a_j` (order them; the second largest is counted once
in the middle sum with the largest, and every smaller one at least once).  For two independent uniform centres,
`E min(e_r(·⊕c), e_r(·⊕c′)) ≤ E[e_r(x⊕c)·1{x ∈ B(c′, r−1)}] = m_r V(n,r−1)/2ⁿ`.  (iii) With `Õ = E_π(Σ_j e_j − max_j e_j) ≤ O_c`:
`‖μ_{w_c} − μ̃_c‖₁ ≤ Õ/(1 + Lm_r − Õ) + (1 + Lm_r)·|1/(1 + Lm_r − Õ) − 1/(1 + Lm_r)| = 2Õ/(1 + Lm_r − Õ)`.  ∎

**Theorem A′ (narrow dips) [P].**  Let `M ≥ 1`, `0 < τ ≤ 1`, `0 < η < 1`, `L ≥ 8τ^{−2}ln(2M/η)` an integer,
and `r` a radius with `L m_r > e^ε − 1 + τ/5`.  Every `(ε/2, δ)`-correct randomised algorithm with an
oracle (O1) makes at the constant weight, with truthful uniform answers,

    E|Q|  ≥  (1 − 2δ)(1 − η − η′) · 2ⁿ / ( L · V(n, r−1) ),      η′ = (5 L m_r / (2τ)) · L V(n, r−1) / 2ⁿ .

*Proof.*  Independent uniform centres.  `E_{μ̃_c}φ − E_πφ = (Lm_r/(1+Lm_r))(L^{−1}Σ_j Z_j − E_πφ)` with
`Z_j = E_ν φ(· ⊕ c_j)`, `ν = e_rπ/m_r`; the `Z_j` are independent, in `[−1, 1]`, with mean `E_πφ` by (2.1).  Let `G`
be the event that `|L^{−1}Σ_j Z_j − E_πφ_i| ≤ τ/2` for all `i` and `O_c ≤ τ/5`.  By Lemma 2.4 and Markov's
inequality with Lemma 2.5(ii), `P(Gᶜ) ≤ 2M e^{−Lτ²/8} + 5L²m_rV(n,r−1)/(2^{n+1}τ) ≤ η + η′`.  On `G`:
`|E_{μ_{w_c}}φ_i − E_πφ_i| ≤ τ/2 + 2·(τ/5)/(1 − 1/5) = τ` (Lemma 2.5(iii)), so the uniform answers are admissible,
and `A(w_c) ≥ 1 + L m_r − τ/5 > e^ε`.  A point lies in `∪_j B(c_j, r−1)` with probability at most
`L V(n,r−1)/2ⁿ`.  Lemma 2.3.  ∎

**Corollary A′ (exponents) [P].**  Let `τ = e^{−γn}`, `ln ln M = βn + o(n)`, `λ = 2γ + β < a`, bounded
accuracy.  Then the adaptive exponent with the oracle is at least

    h̄(λ)  :=  KL(ρ₀ − λ/u ‖ ½) − λ ,          provided  h̄(λ) > γ .

`h̄` is convex and decreasing on `[0, a]`, `h̄(0) = h`, `h̄(a) = 0`, `h̄′(0) = −(1 − ℓ)`; so
`h̄(λ) ≥ h − (1 − ℓ)λ`, against `h − λ` from Theorem A.  At `u = 1`: `1 − ℓ = 0.5100`, and the side
condition holds for `β = 0` up to `γ = 0.01544` (where the bound is `0.0154`), while `h − 2γ` vanishes
at `γ = 0.01457`.

*Proof.*  `L = e^{λn + o(n)}`; `L m_r ≈ 1` gives `r/n → ρ₀ − λ/u > p_u`; `n^{−1}ln(2ⁿ/(L V(n,r))) → ln 2 − λ − h₂(ρ₀ − λ/u)`.
`η′ → 0` iff this exponent exceeds `γ`.  `h̄′(λ) = u^{−1}ln((1−ρ)/ρ) − 1` at `ρ = ρ₀ − λ/u`, `h̄″ = 1/(u²ρ(1−ρ)) > 0`.  ∎

| `γ` (`u = 1`, `β = 0`) | Theorem A: `h − 2γ` | Corollary A′: `h̄(2γ)` | upper bound `(1 − γ/ln 2)h` (§5) |
|---|---|---|---|
| 0 | 0.029139 | 0.029139 | 0.029139 |
| 0.002 | 0.025139 | 0.027133 | 0.029055 |
| 0.005 | 0.019139 | 0.024252 | 0.028929 |
| 0.010 | 0.009139 | 0.019795 | 0.028719 |
| 0.0145 | 0.000139 | 0.016154 | 0.028530 |

The gap between the last two columns is open (§11, problem 1).

### 2.4 Any reference measure, any homogeneous space: the flat mixture

The proof of Theorem A used the uniform measure twice: translations preserve it, and the
average of all translates of a weight is constant.  Only the second matters.

**Lemma 2.6 (flat mixture) [V] (`hiding_law_sum`, `flat_mixture`, `flat_mixture_truncated`).**  Let
`X` be a finite set with a metric `d` such that `Σ₀ := Σ_c e^{−u d(x,c)}` does not depend on `x` (every
vertex-transitive metric space; Hamming spaces over any alphabet; the lemma needs only a kernel
with constant row sums).  Let `π` be **any** probability measure on `X`, `ε₀ > 0`, and

    m(c) = E_π e^{−u d(·,c)},      q(c) = m(c)/Σ₀,      H(c) = ε₀/m(c).

Then `q` is a probability vector and `Σ_c q(c)·H(c)e^{−u d(x,c)} = ε₀` **for every `x`**; and for the dips
`w_c = max(1, H(c)e^{−u d(·,c)})`: `Σ_c q(c)w_c(x) = 1 + ε₀ − δ_tr(x)`, `δ_tr(x) = Σ_c q(c)·min(1, H(c)e^{−u d(x,c)})`.

*Proof.*  `q(c)H(c) = ε₀/Σ₀`.  ∎

`q` is the law of a point of `π` moved by the kernel `e^{−u d}/Σ₀` — **the reference blurred at the
temperature of the class**.  Each `w_c` is an alternative with (almost) the same excess `ε₀` whatever
its centre; drawn from `q`, their average is flat, so its ensemble is the reference itself.

**Theorem A″ [P; Lemma 2.6 V].**  `X`, `d`, `π` as in Lemma 2.6; algorithms are `(ε/2, δ)`-correct for
`ln E_π w` on the admissible class, with an oracle (O1) for the ensembles `wπ/E_π w`.  Let
`ξ̄ = E_π δ_tr`, `B_c = {x : H(c)e^{−u d(x,c)} > 1}`, `P_hit = max_x q({c : x ∈ B_c})`.  If `ε₀ ≥ e^ε − 1 + τ`,
`ξ̄ ≤ τ/4` and `L ≥ 32(ε₀/τ)² ln((2M + 2)/η)`, then at the constant weight, with the answers `E_πφ_i`,

    E|Q|  ≥  (1 − η)(1 − 2δ) / ( L · P_hit ) .

*Proof.*  `c_1, …, c_L` independent with law `q`, `w^{(L)} = L^{−1}Σ_j w_{c_j} ∈ 𝒲_u`.  Then
`E_{μ_{w^{(L)}}}φ = (E_πφ + S_φ)/(1 + S_1)` with `S_φ = L^{−1}Σ_j Y_j`, `Y_j = E_π[(w_{c_j} − 1)φ] ∈ [−ε₀, ε₀]`, and
`S_1 = L^{−1}Σ_j e_j`, `e_j = E_π(w_{c_j} − 1) ∈ [0, ε₀]`.  By Lemma 2.6 `E Y_j = ε₀E_πφ − E_π[φδ_tr]` and
`E e_j = ε₀ − ξ̄`.  On the event that `S_1` and all `S_{φ_i}` are within `τ/4` of their means (probability at
least `1 − (2M+2)e^{−Lτ²/(32ε₀²)} ≥ 1 − η` by Lemma 2.4):
`|E_{μ_{w^{(L)}}}φ_i − E_πφ_i| ≤ |S_{φ_i} − E_πφ_i·S_1| ≤ τ/4 + τ/4 + |E_π[φ_iδ_tr] − E_πφ_i·ξ̄| ≤ τ/2 + 2ξ̄ ≤ τ`, and
`A(w^{(L)}) = 1 + S_1 ≥ 1 + ε₀ − ξ̄ − τ/4 > e^ε`.  `w^{(L)} = 1` off `∪_j B_{c_j}`, which contains a given point
with probability at most `L·P_hit`.  Lemma 2.3.  ∎

**Corollary A″ (any baseline that is a mixture of cones) [P].**  Let `w₀ ∈ 𝒲_u` satisfy
`w₀(x) = Σ_c λ(c)e^{−u d(x,c)}` for all `x`, with weights `λ ≥ 0` (on the cube every `e^{−γ|x|}`, `|γ| < u`, is of
this form with product weights, `λ₁/λ₀ = (1 − e^{−(u+γ)})/(1 − e^{−(u−γ)})` per site).  Then Theorem A″ holds
at the baseline `w₀` for the members `w_c = max(w₀, H(c)e^{−u d(·,c)})`, with `π` replaced by `μ_{w₀}`,
`m(c) = E_π e^{−u d(·,c)}/A(w₀)`, `H(c) = ε₀/m(c)`, the hiding law `q(c) = λ(c)m(c)` and
`B_c = {x : H(c)e^{−u d(x,c)} > w₀(x)}`.  (Apply Lemma 2.6 to the kernel `λ(c)e^{−u d(x,c)}/w₀(x)`, whose rows
sum to one, and the reference `μ_{w₀}`.)

*What this gives, and what it does not.*  (1) On the uniform cube `q` is uniform, `B_c` is a ball
and Theorem A″ is Theorem A up to constants (there `ξ̄ = e^{−nh + o(n)}`).  (2) On any
vertex-transitive space with the uniform measure (slices, Hamming spaces, Cayley graphs with a
word metric, finite homogeneous spaces) the proof of Theorem A applies verbatim with random
group elements: **an oracle (O1) costs at most the factor `L` in the dip-packing bound of that
space** — whether that bound is the true complexity there is a separate question (it is on the
cube).  (3) **For a non-uniform reference the theorem is true but can be weak, and at the
constant baseline it is void at the exponential scale** [N, exact sums over types, `n ≤ 160`,
and a grid evaluation of the exponents: `experiments/phase2/p2_field_flat.py`].  The flat mixture is
unique — the kernel is invertible, so cones must be superposed with equal *heights* — and with a
field this forces centres near the mode of `π`, whose mass-normalised dips are wide: for
`π = Bernoulli(p)ⁿ`, `p ≠ ½`, `−n^{−1}ln P_hit → 0` at the constant weight (`0.015` at `n = 160`, still falling,
for `p = 0.1`, `u = 2`; the worst query is the mode).  Around *tilted* baselines `e^{−γ|x|}` (Corollary A″)
the flat family does give an exponent: its best value over `γ` is `0.0236` at `p = 0.3`, `u = 1` and `0.0203`
at `p = 0.1`, `u = 2`, against `0.0253` and `0.0489` for the best single-type dip family over `γ` on the
same grid (the latter is not hidden from observables: it shifts the magnetisation).  So with
a field **a positive exponent survives every family of `exp(e^{o(n)})` observables at sub-exponential
precision** [P for the bound, N for its value], between 40 % and 95 % of the dip-packing exponent in these two cases; whether the
class exponent itself is invariant is open (§11, problem 4).  For one-body data with a field
exact invariance of both class exponents is known by a different mechanism (compensation; theory
report Theorem 11.109a, science division).

---

## 3. Theorem B: exact observables (the proposed theorem S2)

Walsh characters `χ_s(x) = (−1)^{s·x}`, `s ∈ F₂ⁿ`; `φ̂(s) = E_π φχ_s`.  The **joint spectrum** of observables
`φ_1, …, φ_K` is `S = ∪_i {s ≠ 0 : φ̂_i(s) ≠ 0}`.  For a subgroup `C ≤ F₂ⁿ`, `C^⊥ = {s : s·c = 0 for all c ∈ C}`.

**Lemma 3.1 (invariance kills characters) [V] (`sum_mul_char_eq_zero`,
`ensemble_mean_eq_of_spectrum`).**  If `w(x ⊕ c₀) = w(x)` for all `x` and `χ_s(c₀) = −1`, then `E_π wχ_s = 0`.
Hence if `w` is invariant under a subgroup `C` with `C^⊥ ∩ S = ∅`, then `E_{μ_w}φ_i = E_πφ_i` exactly, for every `i`.

**Lemma 3.2 (a small subgroup avoiding `M` frequencies) [V] (`parity_balanced`,
`exists_separating_tuple`, `exists_generators_cube`).**  For every set `S` of `M` non-zero frequencies
and every `r` with `2^r > M` there are `g_1, …, g_r ∈ F₂ⁿ` such that every `s ∈ S` has `s·g_i = 1` for some `i`.
The subgroup `C` they generate has `|C| ≤ 2^r` and `C^⊥ ∩ S = ∅`; with `r = ⌈log₂(M+1)⌉`: `|C| < 2(M+1)`.

*Proof.*  For `s ≠ 0` exactly half of the points `g` have `s·g = 0`, so `2^{(n−1)r}` of the `2^{nr}` tuples fail
for a given `s`, and `M·2^{(n−1)r} < 2^{nr}`.  ∎

**Theorem B [P; Lemmas 3.1, 3.2 V].**  Let an oracle return the **exact** means `E_{μ_w}φ_i` of
arbitrary real observables whose joint spectrum has `M` elements, and let `C` be any subgroup
with `C^⊥ ∩ S = ∅` (one with `|C| < 2(M+1)` exists).
(a) If `ε < Δ_k`, every `(ε/2, δ)`-correct randomised algorithm makes at the constant weight at least
`(1 − 2δ)·2ⁿ/(|C|·V(n,k))` evaluations in expectation.
(b) For `w₀, w₁ ∈ 𝒲_u` that differ only on `D`, `|ln A(w₁) − ln A(w₀)| > ε`: every non-adaptive
`(ε/2, δ)`-correct algorithm makes at least `(1 − 2δ)·2ⁿ/(|C|·|D|)` evaluations in expectation.
(c) *The bound on `|C|` cannot be improved in general:* if `S = W∖{0}` for a subspace `W` of dimension
`d` (`M = 2^d − 1`), every subgroup with `C^⊥ ∩ S = ∅` has `|C| ≥ 2^d = M + 1`.
(d) Hence exact means of observables with joint spectrum of size `e^{o(n)}` — in particular all
marginals of order `k = o(n)`, `M < V(n,k)` — change neither leading exponent.

*Proof.*  (a) For a centre `a` put `w_a^C = |C|^{−1}Σ_{c∈C} w_{a⊕c, k+1}`: admissible, `A` preserved (Lemma 2.2),
`C`-invariant, so by Lemma 3.1 the oracle's answer is the one at the constant weight; `w_a^C = 1` off
`∪_{c∈C} B(a ⊕ c, k)`, which contains a fixed point for at most `|C|V(n,k)` of the `2ⁿ` centres `a`.
Lemma 2.3 with a functional oracle.  (b) The same with `|C|^{−1}Σ_c w_i(· ⊕ a ⊕ c)`.  (c) `C^⊥ ∩ W = {0}` forces
`dim C^⊥ ≤ n − d`.  (d) (a), (b) and the upper bounds without an oracle.  ∎

**Theorem B′ (refined, by maxima of dips) [P].**  Let `S` be a set of `M` non-zero frequencies,
`K = 2^{⌈log₂(4M)⌉}`, and `r` a radius with `½K m_r > e^ε − 1` and `4K·V(n,r−1) ≤ 2ⁿ`.  Then with the exact
oracle of Theorem B, `E|Q| ≥ (1 − 2δ)·2ⁿ/(K·V(n,r−1))` at the constant weight.  In exponents, for
`M = e^{λn + o(n)}`, `λ < a`: the adaptive exponent is at least `h̄(λ)`.

*Proof.*  Draw `k = log₂K` generators independently and uniformly; `C` their span.  (i) Each
`s ∈ S` lies in `C^⊥` with probability `2^{−k}`, so `P(C^⊥ ∩ S ≠ ∅) ≤ M/K ≤ ¼`.  (ii) Every non-trivial
combination of the generators is uniform on `F₂ⁿ`; for the multiset `C̃` of all `K` combinations,
`O = Σ_{pairs of C̃} E_π min(e_r(·⊕c), e_r(·⊕c′))` has `E O ≤ ½K²m_rV(n,r−1)/2ⁿ ≤ K m_r/8`, so `O ≤ ½K m_r` with
probability at least `¾`.  Fix generators with both properties.  `w_a = 1 + max_{c∈C̃} e_r(· ⊕ a ⊕ c)` is
admissible (Lemma 2.1), `C`-invariant, equals `1` off `K` balls, and `A(w_a) − 1 ≥ K m_r − O ≥ ½K m_r > e^ε − 1`
(Lemma 2.5(ii); `O` does not depend on `a`).  Lemmas 3.1, 2.3.  For the exponent: `K m_r ≈ 1` gives
`r/n → ρ₀ − λ/u`.  ∎

**Corollary B′ (exact marginals of linear order) [P].**  With all marginals of order at most `αn`
given exactly, the adaptive exponent `θ(α)` satisfies

    h̄(h₂(α))  ≤  θ(α)  ≤  (1 − α)·h ,

the lower bound being positive iff `h₂(α) < a`.  At `u = 1`: for `α < α₁ = 0.02339`, against
`α < α₀ = 0.00456` for the bound `h − h₂(α)` of the science division's Theorem 4‴ (addendum A8).
(Upper bound: theirs — fix `αn` coordinates.)  The gap is open; no construction of this kind can
close it, because a `C`-invariant family needs `|C| ≥ V(n, αn/2)` (Rao's bound).

---

## 4. Theorem C: where invariance stops

**Theorem C (the joint law of a block of coordinates) [P, given the cube theorems].**  Let
`0 ≤ b ≤ n` and let the oracle return the law `ν_w` of the first `b` coordinates under `μ_w`, or any
`ν̂` with `‖ν̂ − ν_w‖₁ ≤ τ`.
(a) *Lower bound, even for the exact oracle.*  Every `(ε/2, δ)`-correct algorithm needs at least as
many evaluations as an `(ε/2, δ)`-correct algorithm without oracle on the cube of `n − b` sites:
`E|Q| ≥ (1 − 2δ)2^{n−b}/V(n−b, k)` if `ε < Δ_k^{(n−b)}` (adaptive), and the non-adaptive bound of `n − b` sites.
(b) *Upper bound.*  If `τ ≤ (1 − e^{−ε/4})·δ/2`, the following algorithm is `(ε/2, δ)`-correct: draw a cell
`s ~ ν̂`; run an `(ε/4, δ/2)`-correct algorithm for the cube of `n − b` sites on `y ↦ w(s, y)`, obtaining `Â_s`;
return `ln Â_s − b ln 2 − ln ν̂(s)`.
(c) Hence for `b = θn` and bounded accuracy **the exponents are exactly `(1 − θ)h` (adaptive) and
`(1 − θ)a` (non-adaptive)**, for the exact oracle and for every tolerance `τ ≤ (1 − e^{−ε/4})δ/2`.

*Proof.*  (a) A weight `v` admissible on the last `n − b` coordinates defines the cylinder
`w(s, y) = v(y)`, admissible on `X`, with `A(w) = A(v)` and `ν_w` uniform — the same answer for every
cylinder.  An algorithm restricted to cylinders, with the answer "uniform" built in, is an algorithm
for `n − b` sites.  (b) `A(w) = 2^{−b}·E_y w(s,y)/ν_w(s)` for every cell `s`.  For `s ~ ν̂`:
`P(|ν_w(s)/ν̂(s) − 1| > κ) ≤ κ^{−1}Σ_s |ν_w(s) − ν̂(s)| ≤ τ/κ`; with `κ = 1 − e^{−ε/4}` the error of `ln ν̂(s)` is at
most `ε/4` outside an event of probability `δ/2`.  (c) Theorems 11.25, 11.45, 11.54/11.58 on `n − b` sites.  ∎

**Corollary C (both hypotheses of Theorem A(c) are necessary) [P].**
(i) The law `ν_w` to within `‖·‖₁ ≤ τ` is obtained from an oracle (O1) with the `M = 2^{2^b}` indicator
functions of unions of cells at tolerance `τ/4` (two laws that agree on every union to within `τ/2`
differ by at most `τ` in `‖·‖₁`).  So with `ln ln M = θn·ln 2` and *constant* tolerance
the adaptive exponent drops to `(1 − θ)h`: **`ln ln M = o(n)` cannot be dropped.**
(ii) It is also obtained from the `2^b` indicator functions of the cells at tolerance `τ2^{−b}`.  So with
`M = e^{γn}` observables at tolerance `e^{−γn − O(1)}` the exponent is at most `(1 − γ/ln 2)h`:
**`ln(1/τ) = o(n)` cannot be dropped.**  With adaptive statistical queries (O2), `b` queries suffice
(halving, keeping the heavier half).
(iii) Consequently `(1 − γ/ln 2)h` is an upper bound for the exponent in the regime of Corollary A′.

**Proposition C′ (the full oracle; one exact number) [P].**
(a) Let the oracle return any `μ̂` with `‖μ̂ − μ_w‖₁ ≤ τ` (this is what all indicator functions at
tolerance `τ/4` give).  Draw `x_1, …, x_k ~ μ̂` independently and return the median of
`ln w(x_i) − n ln 2 − ln μ̂(x_i)`.  Each term is within `ε/2` of `ln A(w)` unless `|μ_w(x_i)/μ̂(x_i) − 1| > κ := 1 − e^{−ε/2}`,
which has probability at most `τ/κ`; so `k` evaluations are `(ε/2, δ)`-correct as soon as
`(4τ/κ)^{k/2} ≤ δ`: **`O(ln(1/δ)/ln(κ/τ))` evaluations, independently of `n`.**
(b) One exact value `μ_w(z)` and one evaluation give `A(w) = w(z)2^{−n}/μ_w(z)`.  So for *exact*
observables the size of the spectrum in Theorem B is the right parameter: the indicator of a point
has full spectrum.
(c) *Deterministic algorithms do not profit in the same way.*  For a deterministic algorithm with
any oracle (O1)/(O2) of tolerance `τ`, any number of observables: let it evaluate the set `Q` at the
constant weight (uniform answers), and put `ρ = ⌈Δ/u⌉ − 1`, `Δ = ε + ln 2`, `p = π(∪_{x∈Q} B(x, ρ))`.  The
weight `w = min(e^Δ, e^{u·d(·,Q)})` is admissible, equals `1` on `Q`, and has `A(w) > e^Δ(1 − p)` and
`TV(μ_w, π) ≤ p/(1 − p)`.  If `p ≤ τ/3`, every answer given at the constant weight is admissible for `w`
(`2p/(1−p) ≤ τ`) and `A(w) > e^ε`, so the algorithm errs; hence `|Q| ≥ (τ/3)·2ⁿ/V(n, ρ)`.  Conversely, for
`τ ≤ κ/8`, `κ = 1 − e^{−ε/4}`: `b = ⌊log₂(κ/(8τ))⌋` halving queries (indicators of subcubes, keeping the half
with the larger reported mass) find a subcube `T` of codimension `b` with `μ_w(T) ≥ 6τ/κ`, known to
relative accuracy `κ/6`, and a `⌊ε/(4u)⌋`-net of `T` determines `E_π[w1_T]` to within `e^{±ε/4}`:
`2^{n−b} ≤ (16τ/κ)·2ⁿ` evaluations.  **Deterministic cost with observations at tolerance `τ`: `τ·2ⁿ` up to
factors polynomial in `n`** — the tolerance buys exactly its own factor, whatever is observed.

*Reading.*  Rows A, C, C′ together: for randomised algorithms the value of averaged data is
governed by `τ^{−2}ln M` — the number of *samples of the hidden structure that the data cannot tell
from the continuum* — and it is negligible, a constant fraction of the exponent, or everything,
according to whether `ln(τ^{−2}ln M)` is `o(n)`, `Θ(n)`, or `n ln 2`.

---

## 5. The exponentially precise regime: what is known

`τ = e^{−γn}`; randomised algorithms; bounded accuracy; `u = 1` for numbers.

| observables | lower bound for the exponent | upper bound | source |
|---|---|---|---|
| any `M = e^{o(n)}` fixed, or `q = e^{o(n)}` adaptive | `max(h − 2γ, h̄(2γ)·1[h̄(2γ) > γ])` | `(1 − γ/ln 2)h` if the family contains cell indicators | A, A′, Corollary C |
| all Walsh characters | the same (improves the science division's A10, where `τ ≥ e^{−o(n/ln n)}` was needed and the crossover was left open) | — | A′ |
| non-adaptive algorithms | `a − 2γ` | `(1 − γ/ln 2)a` | A(b), C |
| exact, spectrum `e^{λn}` | `h̄(λ)` | `(1 − λ/ln 2)h` when the spectrum is a coordinate subspace (exact) | B′, C |
| deterministic algorithms | `ln 2 − γ` | `ln 2 − γ` | C′(c) |

The slopes at `γ = 0` are `−2(1 − ℓ) = −1.02` (lower) and `−h/ln 2 = −0.042` (upper).  Which is right
is the main open problem of this report.  What the two bounds use: the lower bound hides
`e^{2γn}` narrow dips at random; the upper bound zooms into a subcube, where dips *centred in the
subcube* are over-represented and a smaller radius matters.

### 5.1 One criterion behind Theorems A, B and the science division's Theorem 4-τ

For a probability measure `ρ` on centres write `ρ̃(s) = Σ_c ρ(c)χ_s(c)` (its bias at the frequency `s`), and
let `ν` be the normalised excess of a dip, `ν̃(s)` its bias.  Let `Γ` be a finite set of centres, `ρ_Γ` the
uniform measure on it, and `ν_{Γ⊕a} = |Γ|^{−1}Σ_{c∈Γ} ν(· ⊕ c ⊕ a)` the excess of the dips at `Γ ⊕ a`.

**Lemma 5.1 (attenuated bias) [P; checked exactly on a cube of 8 sites].**  For every `φ` and a uniform shift `a`,

    E_a ( E_{ν_{Γ⊕a}} φ − E_π φ )²  =  Σ_{s ≠ 0} φ̂(s)² · ρ̃_Γ(s)² · ν̃(s)²   ≤   E_π φ² · max_{s ≠ 0} ( |ρ̃_Γ(s)| · |ν̃(s)| )² ,

with equality in the second place for `φ = χ_s` at a maximising `s`.  Moreover `|ν̃(s) − t^{|s|}|` is
exponentially small at the critical radius, `t = tanh(u/2)` (the science division's attenuation lemma A10.2
**[K]**): *thermal noise attenuates a test of order `j` by `t^j`*.

*Proof.*  `E_{ν_{Γ⊕a}}φ = Σ_s φ̂(s)ρ̃_Γ(s)ν̃(s)χ_s(a)` (the bias of a convolution is the product of the biases; a
shift multiplies by `χ_s(a)`), and the characters are orthonormal in `a`.  ∎

So, by Chebyshev's inequality, a family of dips at `Γ ⊕ a` is hidden from a given observable at
tolerance `τ` with probability `1 − η` as soon as its **attenuated bias** `β(Γ) = max_{s≠0}|ρ̃_Γ(s)|·t^{|s|}` is at
most `τ√η`, and it is not hidden from the character at the maximising frequency if `β(Γ) > τ`.  The
three known constructions are the three ways of making `β` small:

| centres `Γ` | bias `ρ̃_Γ(s)` | atoms needed |
|---|---|---|
| `L` independent uniform points (Theorem A) | of size `L^{−1/2}` at every `s` | `τ^{−2}` (times `ln M` for `M` observables, by Hoeffding instead of Chebyshev) |
| a subgroup `C` (Theorem B) | the indicator of `C^⊥` | zero error for every observable whose spectrum avoids `C^⊥`: `< 2(M+1)` |
| a linear code of dual distance `k_τ = ln(1/τ)/ln(1/t)` (science division, Theorem 4-τ) | the indicator of `C^⊥`, attenuated by `t^{|s|} ≤ τ` on it | between `V(n, k_τ/2)` (Rao) and `e^{n h₂(k_τ/n)}` (Gilbert–Varshamov) |

For `τ = e^{−γn}` with small `γ` the first is the cheapest (`e^{2γn}` against `e^{n h₂(κ)}`,
`κ = γ/ln coth(u/2)`), and unions of `m` random cosets of a code of dual distance `J` cost
`V(n, J/2)·τ^{−2}t^{2J}`, which is increasing in `J` at `J = 0`: **no hiding family of this kind has fewer than
about `τ^{−2}` atoms at small `γ`.**  Whether fewer atoms can hide (a set with attenuated bias `τ` and
`τ^{−2+c}` points), or whether, conversely, an algorithm can turn the detectable bias of a smaller
family into a *localisation* of its dips — detection is not localisation: for `L` random dips the
one-body biases are of size `L^{−1/2}` and tilt the density of centres by `e^{n/√L}` only — is exactly
the open problem (§11, problem 1).

---

## 6. Theorem E: samples from the ensemble

**Model.**  Before any evaluation the algorithm receives `m` independent samples of `μ_w` (snapshots
of the ensemble).  This is not a mean: one sample lands in a hidden dip of constant excess with
constant probability, and the family of Theorem A is not hard at all against it (the science
division's remark after its Theorem 4-τ).

**Theorem E [P].**  Let `0 < η₁ ≤ 1/40`, `K = ⌈m²/η₁⌉`, and `r` a radius with `R := K m_r ≥ m/η₁`, and suppose
`N* := 2ⁿ/(K V(n, r−1)) ≥ 40m/η₁`.  Every randomised algorithm that is `(ε/2, δ)`-correct with `m` samples,
`ε < ln(11/8)`, makes at least `(1 − 2δ − 12η₁)·N*` evaluations in expectation on some instance.  In
exponents: with `m = e^{νn}` samples, `ν < ν*`,

    n^{−1} ln E|Q|  ≥  h̄(ν) − ν − o(1) ,        where  h̄(ν*) = 2ν* ;

so the total number of samples and evaluations has exponent at least `ν*`.  At `u = ½, 1, 2`:
`ν* = 0.003097, 0.011726, 0.038738`, that is `0.404h, 0.402h, 0.398h`.

*Proof.*  Centres `c_1, …, c_{2K}` independent and uniform; `w₀ = 1 + max_{j≤K} e_r(· ⊕ c_j)`,
`w₁ = 1 + max_{j≤2K} e_r(· ⊕ c_j)` (Lemma 2.5).  *Values.*  `A(w₀) ≤ 1 + R` and `A(w₁) ≥ 1 + 2R − O₁`; by Lemma
2.5(ii) and Markov `P(O₁ > R/4) ≤ 8K V(n,r−1)/2ⁿ ≤ η₁/5`; otherwise `A(w₁)/A(w₀) ≥ (1 + 7R/4)/(1 + R) ≥ 11/8 > e^ε`
(`R ≥ 1`).  *Samples.*  By Lemma 2.5(iii) a sample of `μ_{w_i}` can be coupled with a sample of the
ideal mixture `μ̃_i` — "the floor" (a uniform point) with probability `1/(1 + K_i m_r)`, otherwise a
uniformly chosen centre `c_j` plus an independent displacement with law `ν = e_rπ/m_r` — except with
probability `TV(μ_{w_i}, μ̃_i)`, whose expectation is at most `2K_iV(n,r−1)/2ⁿ`.  For `m` ideal samples:
`P(some sample on the floor) ≤ m/R ≤ η₁` and `P(two samples from the same centre) ≤ m²/(2K) ≤ η₁/2`.
Conditionally on neither, the sampled centres are `m` independent uniform points, the
displacements are independent with law `ν`, and the unsampled centres are independent and
uniform — `K − m` of them under `w₀`, `2K − m` under `w₁`.  So the two experiments can be realised on one
probability space with the same samples and the same sampled centres, the unsampled centres of
`w₀` being a subset of those of `w₁`, outside an event of probability at most
`(η₁ + η₁/2) + (η₁/2 + η₁/4) + 6mK V(n,r−1)/2ⁿ < 2.5η₁` (bad sampling in either experiment).  *Evaluations.*  On that space run the algorithm on
`w₀`; the `K` centres that `w₁` has in addition are independent of that run, so the probability that
one of its evaluations falls within distance `r − 1` of one of them is at most `E|Q₀|·K V(n,r−1)/2ⁿ = E|Q₀|/N*`;
if none does, the run on `w₁` is the same run and returns the same number.  Both cannot be
correct when `A(w₁)/A(w₀) > e^ε`.  The run on `w₀` errs with probability at most `δ`; the coupled run on
`w₁` errs with probability at most `δ` plus the distance between the coupled experiment and the
true one (at most the bad-sampling probabilities, `< 2.5η₁`).  Collecting:
`1 − 1.55η₁ − 0.2η₁ − E|Q₀|/N* ≤ 2δ + 2.5η₁`, that is `E|Q₀| ≥ (1 − 2δ − 4.25η₁)N*`; the statement has `12η₁` to
leave room.  The bound is for the average over the random instance `w₀`, hence for some instance.
*Exponents.*  `K = e^{2νn}`, `m_r ≈ 1/m` gives `r/n → ρ₀ − ν/u`, and
`n^{−1}ln N* → ln 2 − 2ν − h₂(ρ₀ − ν/u) = h̄(ν) − ν`; the condition `N* ≥ 40m/η₁` is `h̄(ν) > 2ν`.  ∎

*Remarks.*  (1) The two mechanisms are the birthday bound (`m² ≪ K`: no two samples share a
basin, so the number of basins is invisible) and hiding (the basins not sampled must be found
by evaluations).  The family must be a *maximum* of dips, not an average: exact evaluations near
a sampled centre would reveal the scale `1/K` of an averaged dip.  (2) In terms of `m`:
`N ≳ N₀/m^{2−ℓ}` — a sample is worth at most `m^{1−ℓ}` per sample, against `(τ^{−2}ln M)^{1−ℓ}` for means.
(3) **No algorithm is known that uses samples to beat `e^{nh}` on the whole class**
[open: §11, problem 2].  The identity `A = E_π[w·1_T]/μ_w(T)` with `T = {w ≤ θ}` costs `1/μ_w(w ≤ A)` samples, which at
the cone is again `e^{nh}` (`h` is the Chernoff information between `π` and the cone's ensemble).
With samples of *pinned* ensembles the problem is polynomial (self-reducibility; science
division, addendum A7).

---

## 7. A hierarchy of information operators

Cost of `ln A` to bounded accuracy on the cube class, randomised algorithms, leading exponent.

| operator | exponent | reference |
|---|---|---|
| evaluations only | `h` (adaptive), `a` (fixed sample) | theory report §§11.10–11.19 |
| + means of `M` observables at tolerance `τ`, `ln(τ^{−2}ln M) = o(n)` | unchanged | Theorem A |
| + the same with `ln(τ^{−2}ln M) = λn` | in `[h̄(λ), (1 − γ/ln 2)h]` | A′, C |
| + exact means, joint spectrum `e^{λn}` | `≥ h̄(λ)`; `= (1 − θ)h` for the law of `θn` coordinates | B′, C |
| + exact marginals of every order `≤ αn` | in `[h̄(h₂(α)), (1 − α)h]` | Corollary B′ |
| + the mean energy (calorimetry) | `h` in the worst case | science division, Proposition 5b |
| + `e^{νn}` samples | in `[h̄(ν) − ν, h]`; total cost `≥ ν*` | Theorem E |
| + all bounded observables at tolerance `τ ≤ cεδ` | `0` (a bounded number of evaluations) | Proposition C′(a) |
| + one exact point probability | `0` (one evaluation) | Proposition C′(b) |
| + samples or one-body marginals of pinned ensembles | `0` (polynomial) | science division A7 [K] |

---

## 8. Sharp characterisations for experimentally motivated operators (objective 5): status

*Sharp (two-sided, exponent level):* means with error bars in the sub-exponential regime
(Theorem A: nothing); the exact or approximate joint law of a block of sites (Theorem C:
`(1 − θ)h`); the full oracle (C′); deterministic algorithms with any observations (C′(c): `ln 2 − γ`).
*Two-sided with a gap:* exponentially precise means; exact marginals of linear order; samples.
*One further consequence of Theorem A, stated because it is the experimentally relevant one:* a
histogram of an order parameter — the law under `μ_w` of a statistic with `P` values, to
total-variation tolerance `τ` — is an oracle (O1) with `M = 2^P` observables, so it costs at most the
factor `2τ^{−2}(P ln 2 + ln(4/η))`: **a histogram with polynomially many bins and constant error bars
changes no exponent**, whatever the order parameter (the magnetisation, a contact count, a
distance), while the *exact* law of the magnetisation makes the problem trivial (one evaluation at
the all-zero state).  Exactness, not order or locality, is what makes averaged data informative.

---

## 9. Verdict on S1 and S2, and what is new against the archive

**S1 — correct.**  Statement and proof strategy are right, including the constant
`L ≥ (2/τ²)ln(4M/η)`, the bound `E Q ≥ (1 − η)(1 − 2δ)2ⁿ/(L|B|)` and the exponents `max(0, h − 2γ)`, `max(0, a − 2γ)`
as *lower* bounds.  Points that needed care, all resolved in Theorem A: the oracle must be allowed to
return any admissible vector, and the lower bound is proved against the oracle that returns the
uniform means; the good event is conditioned on by restricting the alternatives (Lemma 2.3), which
costs the factor `1 − η`, not `1/(1 − η)` in the hitting probability; for the adaptive pair only one
family has to concentrate (`ln(2M/η)`), and its range is `2(1 − e^{−Δ})`; the bound is on the expected
cost at the baseline with truthful answers.  Strengthened: adaptive statistical queries; any
homogeneous space; any reference measure (flat mixture); the exponent `h̄(2γ + β)` in place of
`h − 2γ − β`; necessity of both conditions; the collapse beyond them.
**S2 — correct.**  `r = ⌈log₂(M+1)⌉` generators, a subgroup with `|C| ≤ 2^r < 2(M+1)` whose dual avoids `S`,
loss at most `|C|`.  Strengthened: arbitrary exact observables through their joint spectrum;
optimality of the bound on `|C|`; the exponent `h̄(λ)`; the sharp value for a block of coordinates.

**Against the archive** (science division, `INFERENCE_LIMITS.md` and addenda; theory report §§11.27, 11.29).

| statement here | what the archive has | what is new |
|---|---|---|
| Theorem B(d): exact marginals of order `o(n)` change no exponent | Theorem 4 with BCH codes (`k = o(n/ln n)`), addendum A1 / Proposition 11.104 (non-adaptive), Theorem 4‴ of A8 with Gilbert–Varshamov (which covers `k = o(n)` for the adaptive exponent) | **nothing in substance** — S2's corollary is theirs |
| Theorem B(a)–(c): any frequency set, any exact observables by spectrum, optimal `\|C\|` | Lemma 1 (dual distance) | the formulation by spectrum; the random-subgroup bound `2(M+1)` and its optimality |
| Corollary B′: `θ(α) ≥ h̄(h₂(α))` | `θ(α) ≥ h − h₂(α)` (A8), "the gap between the bounds is open" | the lower bound; positive range `α < 0.0234` instead of `0.0046` (`u = 1`) |
| Theorem A: arbitrary bounded observables, tolerance `τ`, both exponents | Theorem 4-τ (A10): Walsh characters of every order, `τ ≥ e^{−o(n/ln n)}`, adaptive exponent, by a code and the attenuation `tanh(u/2)^j` | arbitrary observables and the count `M`; the range `ln(1/τ) = o(n)`; the non-adaptive exponent; a different mechanism (random translates) |
| Corollary A′ | A10 remark (2): "the crossover — tolerance `e^{−γn}` — is open" | two-sided bounds in the crossover |
| Theorem A″, Lemma 2.6 | compensation for one-body data with a field (Theorem 11.109a) | every bounded observable, every reference measure — at the price of a non-optimal exponent off the uniform cube |
| Theorems C, C′, E | the upper bound `(1 − α)h` for marginals of order `αn` (A8); the remark that a sampler finds the dips (A10) | the matching lower bound for a block; necessity of S1's hypotheses; the full-oracle collapse and its deterministic counterpart; the sample lower bound |

**Prior art outside the programme** (from memory and one bounded search — §12; nothing below was
found stated for free energies of Lipschitz classes).  Statistical-query learning: `O(τ^{−2}log M)`
samples answer `M` statistical queries (Kearns 1998) — Theorem A uses the same count in the opposite
direction, for an adversary.  Averaging over a code to kill low-order statistics: orthogonal
arrays, `k`-wise independence (Rao 1947; Alon–Babai–Itai 1986); the random-subgroup argument of
Lemma 3.2 is the Gilbert–Varshamov argument for linear codes.  Counting versus sampling:
Jerrum–Valiant–Vazirani 1986.  Birthday-type lower bounds for estimating support size from
samples: Raskhodnikova–Ron–Shpilka–Smith 2009; Valiant–Valiant 2011.  **Every ingredient is
classical; the statements are, to our knowledge, not in print for this problem.  "Not found" is
not "new".**

---

## 10. Verification status

| item | status |
|---|---|
| Lemmas 2.1, 2.2, 2.3, 2.6, 3.1, 3.2; the form of 2.4 used | **[V]** `proofs/Frontiers/ObservationInvariance.lean` (registered in `proofs/AxiomAudit.lean`) |
| Theorems A, A′, A″, B, B′, C, C′, E | **[P]** this file; the reductions to the lemmas are short, the asymptotics are binomial estimates |
| every identity and inequality of §§2–6 on small cubes; the exponent functions | **[N]** exact enumeration, `experiments/phase2/p2_checks.py` (31 checks) and harness block XXVIII (four tests, 21 mutations, all caught) |
| internal review | one adversarial AI referee — see `docs/phase2/PHASE2_REVIEW.md` when present |
| upper bounds | rest on the cube theorems 11.44, 11.54, 11.58 ([P], refereed internally) |

## 11. Open problems

1. **The exponent at tolerance `e^{−γn}`**: between `h̄(2γ)` and `(1 − γ/ln 2)h` (§5).  Equivalently:
   what is the least number of atoms of a hiding family that fools every bounded observable to
   `τ` — `τ^{−2}` (random), or fewer with structure?
2. **Samples**: is there an algorithm with samples below `e^{nh}` on the whole class?  Lower bound
   `ν* ≈ 0.40h`.
3. **Exact marginals of linear order**: `[h̄(h₂(α)), (1 − α)h]`.
4. **Non-uniform references**: the optimal flat family (baseline and mixture) for a field; is the
   class exponent with a field invariant under arbitrary bounded observables?  Chains.
5. **Homogeneous spaces**: on which transitive spaces is the dip-packing bound the adaptive
   complexity?  (Then Theorem A is an invariance theorem there, as on the cube.)
6. Machine-checking the passage from the cores to the displayed bounds of Theorems A and B on the
   cube (finite `n`; needs the product measure on `X^L`), and any upper bound.
