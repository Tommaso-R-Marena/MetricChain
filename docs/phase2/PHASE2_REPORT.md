# Phase II — what observational information is worth to a certified free energy

*Theoretical Research Division, branch `research/phase2-foundations`, 2026-11-28.  Written under
the research owner's directive "MetricChain Phase II — Foundational Mathematics and General
Information Complexity".  Everything here was produced by an AI session; "refereed" means read by
another AI session.  **No statement has been read by a human expert.**  Status labels as in the
theory report: **[V]** machine-checked in Lean (the statement is exactly the Lean statement),
**[P]** paper proof in this file, **[N]** numerical evidence, **[K]** cited, **[C]** conjecture.*

*Review.*  One adversarial AI referee read the first version (`docs/phase2/PHASE2_REVIEW.md`; replications
under `experiments/phase2/review/`).  Its verdict: every numbered theorem stands; **two numerical claims of
§2.4 about the flat family with a field were wrong** (an extrapolation from `n ≤ 160` — "void at the constant
baseline" — and product weights that were inverted); one constant in a statement (Theorem A for adaptive
queries) was not what its proof gives; Lemma 2.5 (iii) lacked a proviso; Theorem E was quoted for a wider
range of accuracies than it was proved for; a halving protocol needs `2b` queries, not `b`; one statement
(C′ (b)) is the archive's; several sentences said more than the proofs.  All are corrected below, and
`docs/DEAD_ENDS.md` D71 records the two errors.  Lemma 5.1 and Proposition 2.7 were added during the
review and were read by the referee ("correct as stated").

*After the review.*  **Theorem A′ and Corollary A′ (§2.3) were strengthened on 2026-11-28, after that
review**: the side condition `h̄(λ) > γ` of the first version is removed, so that the lower bound `h̄(2γ)` at
tolerance `e^{−γn}` holds for every `γ < a/2` (at `u = 1`: up to `0.0555` instead of `0.0154`).  The first
referee did not see the new proof.  A second, short review of exactly that section
(`docs/phase2/PHASE2_REVIEW_A1.md`; replications `experiments/phase2/review/a1_*`) found the new theorem, its
lemma and its corollary correct, except in a degenerate corner of the statement (`δ > ½`; now excluded), and
supplied a sharper constant; its seven findings are incorporated, and it read the corrected section and
the remark on homogeneous spaces once more (§2.3, Note; §10).

*After the owner's collaboration update of 2026-11-28* (a fourth Phase II division, certified MBAR): the
relations between its statements and ours are in a separate note, `docs/phase2/BRIDGE_NOTE.md` — the
overlap of the reference with every ensemble of the class (Theorem F), samples in place of adaptivity
(Corollary F1), the price of a sample (Proposition F2), observables of the energy with a sharp
threshold (Theorem J).  **That note has had no referee**; the two reviews above predate it.  Its results
appear below only as two rows of the table of §7 and in §11.

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
| **A** | means of `M` arbitrary observables `φ_i : X → [−1,1]`, each to absolute tolerance `τ` (answers adversarial inside the tolerance) | at most the factor `L = ⌈2τ^{−2} ln(4M/η)⌉`: `N ≥ (1−η)(1−2δ)·N₀/L` for both lower bounds (`N₀ = 2ⁿ/\|B\|` adaptive, `2ⁿ/\|D\|` non-adaptive).  **Both exponents unchanged if `ln(1/τ) = o(n)` and `ln ln M = o(n)`** — S1 is correct — **and neither condition can be dropped** (row C) | [P]; cores [V] |
| **A′** | the same, exponentially precise: `τ = e^{−γn}`, `ln ln M ≈ βn`, `λ = 2γ + β` | adaptive exponent `≥ h̄(λ) := KL(ρ₀ − λ/u ‖ ½) − λ = h − (1−ℓ)λ + O(λ²)` for every `λ < a` — positive on that whole range (S1's argument gives `h − λ`, positive for `λ < h` only); `ℓ = u^{−1}ln((1−ρ₀)/ρ₀)` is the Chernoff parameter (`0.4900` at `u = 1`).  Upper bound `(1 − γ/ln 2)h`.  Non-adaptive: `≥ a − λ`, `≤ (1 − γ/ln 2)a` | [P]; gap open |
| **A″** | the same on any vertex-transitive finite metric space and for **any reference measure `π`** (any known part) | `N ≥ (1−η)(1−2δ)/(L·P_hit)`; hidden centres are drawn from the *thermally blurred reference* `q ∝ π ∗ e^{−u d}` — the unique law for which mass-normalised cones add up to a constant.  For homogeneous references: the factor `L` in the dip-packing bound of the space (on the cube: the exponents `h`, `a`); with a field a positive but smaller exponent at every baseline `e^{−γ\|x\|}`, the constant one included: 49 % and 22 % of the class exponent in two cases (§2.4) | [P]; identity [V] |
| **2.7** | the same for a **dependent reference** `π ∝ e^{−f}`, `f` any known `κ`-Lipschitz energy (`κ < u`) | sandwich by absorption: lower bounds at the slope `u − κ`, upper bounds at `u + κ`; so `h(u − κ) ≤` exponent `≤ h(u + κ)`; the lower bound also with observations in the regime of row A | [P] |
| **B** | **exact** means of any observables whose joint Walsh spectrum has `M` non-zero frequencies | at most the factor `\|C\| < 2(M+1)` (S2 is correct); refined: exponent `≥ h̄(ln M/n)`.  For the subgroup method the bound on `\|C\|` is tight up to the factor 2 (`S = W∖{0}`, `W` a subspace: least `\|C\| = M + 1`) | [P]; cores [V] |
| **C** | the exact joint law of `b = θn` coordinates (or that law to total-variation `τ ≤ c·εδ`; `M = 2^{2^b}` unions of cells) | **exponent exactly `(1 − θ)h`** (and `(1 − θ)a` non-adaptively) — so `ln ln M = o(n)` cannot be dropped from A | [P] |
| **C′** | every bounded observable to a tolerance `τ` below a constant multiple of `ε` | **`O(ln(1/δ)/ln(κ/τ))` evaluations**, `κ = 1 − e^{−ε/2}`, suffice for randomised algorithms; deterministic ones still need `τ·2ⁿ` up to polynomial factors.  One exact point probability: one evaluation (the science division's, A8) | [P] |
| **E** | `m = e^{νn}` independent samples of the ensemble | for accuracies `ε < ln(11/8)` (any bounded accuracy with the variant of Remark (4)): `N ≥ exp(n[h̄(ν) − ν] − o(n))` for `ν < ν*`, `h̄(ν*) = 2ν*`; hence samples plus evaluations cost at least `e^{ν* n}`, `ν* = 0.4024·h` at `u = 1`.  Upper bound: `h` (no better algorithm known) | [P] lower; gap open |

In one sentence: *on the uniform cube, averaged data whose error bars may hide any value within `τ`
are worth at most a factor `τ^{−2} ln M` — whatever is measured — and this stops being negligible only
when the precision or the logarithm of the number of observables becomes exponential in the size of
the system; the hiding distribution that proves it is the reference ensemble blurred at the
temperature of the class.*  (The tolerance is adversarial.  For independent statistical noise of size
`τ` on each reported mean the count enters differently — `M` noisy copies of one observable average to
`τ/√M` — and nothing is claimed.  With a non-uniform reference only a positive exponent is proved, not
invariance.)

Machine-checked cores: `proofs/Frontiers/ObservationInvariance.lean` (§10).  Exact small-cube
checks of the identities and inequalities listed in its output: `experiments/phase2/p2_checks.py`; harness block
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
admissible for both members.  (For a functional oracle this is Lemma 1 of the science division's workstream F —
`lemma1a`, `lemma1b` in `OracleLowerBound.lean`, not the orthogonal-array Lemma 1 of its `INFERENCE_LIMITS.md`; the proof is the same reduction to the packing bound without an oracle,
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

evaluations in expectation.  With an oracle (O2) making at most `q` statistical queries and
`L ≥ 2τ^{−2}(1 − e^{−Δ_k})² ln(2q/η)`: `E|Q| ≥ (1 − η − 2δ)·2ⁿ/(L·V(n,k))`.
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

For (O2): define the oracle at `w^c` once and for all — *a query `φ` is answered by `E_πφ` if
`|E_πφ − E_{μ_{w^c}}φ| ≤ τ`, and by the true mean otherwise*; it is admissible and does not depend on the
seed.  Fix the seed `ω`.  In the run at the constant weight in which every statistical query is
answered by the uniform mean, the queried functions `φ_1^ω, …, φ_q^ω` are determined by `ω` alone.
The run at `w^c` coincides with it as long as no evaluation falls in `D_c`, provided `c ∈ G_ω` (the event
`G` for `φ_i^ω`: then this oracle gives the uniform answers along the run), and `P_c(G_ω) ≥ 1 − η` for
every `ω`.  The two outputs cannot both be correct, so for every `c`
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

**Lemma 2.5 (maxima of dips) [P; (i) V; of (iv) the mean-zero identity V; (ii)–(iv) checked exactly on small cubes].**  For
`c = (c_1, …, c_L)` put `w_c = 1 + max_j e_r(· ⊕ c_j)`.  (i) `w_c ∈ 𝒲_u`, and `w_c = 1` off `∪_j B(c_j, r−1)`.
(ii) `L m_r − O_c ≤ A(w_c) − 1 ≤ L m_r` with `O_c = Σ_{j<j′} E_π min(e_r(·⊕c_j), e_r(·⊕c_{j′}))`, and for
independent uniform centres `E O_c ≤ C(L,2)·m_r·V(n,r−1)/2ⁿ`.  (iii) With the probability measure
`μ̃_c = (π + Σ_j e_r(·⊕c_j)π)/(1 + L m_r)`: `TV(μ_{w_c}, μ̃_c) ≤ Õ_c/(1 + L m_r − Õ_c)`,
`Õ_c = E_π(Σ_j e_j − max_j e_j) ≤ O_c`; hence `≤ O_c/(1 + L m_r − O_c)` whenever `O_c < 1 + L m_r`.
(iv) *No bias on average; bounded differences.*  For `ψ` with `E_πψ = 0` put `G_ψ(c) = E_π[(w_c − 1)ψ]`, so that
`E_{μ_{w_c}}φ − E_πφ = G_ψ(c)/A(w_c)` for `ψ = φ − E_πφ`.  For independent uniform centres `E_c G_ψ(c) = 0` —
overlaps included — and if `c` and `c′` differ in one centre only, `|G_ψ(c) − G_ψ(c′)| ≤ (sup ψ − inf ψ)·m_r`
(attained when `2(r − 1) < n`: one dip, two antipodal centres, `ψ` the difference of the indicators of the two balls).

*Proof.*  (i) `w_c` is the maximum of the dips `w_{c_j, r}`.  (ii) For nonnegative numbers
`Σ_j a_j − Σ_{j<j′} min(a_j, a_{j′}) ≤ max_j a_j ≤ Σ_j a_j` (order them; the second largest is counted once
in the middle sum with the largest, and every smaller one at least once).  For two independent uniform centres,
`E min(e_r(·⊕c), e_r(·⊕c′)) ≤ E[e_r(x⊕c)·1{x ∈ B(c′, r−1)}] = m_r V(n,r−1)/2ⁿ`.  (iii) With `Õ = E_π(Σ_j e_j − max_j e_j) ≤ O_c`:
`‖μ_{w_c} − μ̃_c‖₁ ≤ Õ/(1 + Lm_r − Õ) + (1 + Lm_r)·|1/(1 + Lm_r − Õ) − 1/(1 + Lm_r)| = 2Õ/(1 + Lm_r − Õ)`.
(iv) `E_π[w_cφ] − A(w_c)E_πφ = E_π[w_cψ] = E_π[(w_c − 1)ψ]`.  For every fixed `x` the tuple `(x ⊕ c_j)_j` has the law of
`(c_j)_j`, so `κ := E_c max_j e_r(x ⊕ c_j)` does not depend on `x`, and `E_c G_ψ = κ·E_πψ = 0`.  Fix all centres
but the `j`-th and let `b = max_{i≠j} e_r(·⊕c_i)` (`b = 0` if `L = 1`).  Then `w_c − 1 = b + D` with
`D = (e_r(·⊕c_j) − b)₊`, `0 ≤ D ≤ e_r(·⊕c_j)`, so `G_ψ(c) = E_π[bψ] + E_π[Dψ]`: the first term does not depend on
`c_j`, and the second lies in `[m_r inf ψ, m_r sup ψ]`, because `0 ≤ E_πD ≤ m_r` and `inf ψ ≤ 0 ≤ sup ψ`.  (The
decomposition and the sharp constant are the second referee's, `PHASE2_REVIEW_A1.md` finding 7; the cruder
bound `2‖ψ‖_∞ m_r` follows from the fact that a maximum is 1-Lipschitz in each argument, which is the
machine-checked form, `abs_sup'_sub_sup'_le`.)  ∎

**Theorem A′ (narrow dips) [P; uses the bounded-differences inequality, K; in this form written after the first
review and reviewed separately, see the note below].**
Let `M ≥ 1`, `0 < τ ≤ 1`, `0 < η < 1`, `δ ≤ ½`, and let the radius `r ≥ 1` and the integer `L ≥ 1` satisfy, with
`R := L m_r`,

    R ≥ 2(e^ε − 1)        and        2 R m_r ln(2M/η) ≤ τ²

(equivalently `m_r ≤ τ²/(2R ln(2M/η))`, so that every single dip is below the tolerance, `m_r < 0.85τ`; for a given radius,
`2(e^ε − 1)/m_r ≤ L ≤ τ²/(2m_r² ln(2M/η))`).  Every `(ε/2, δ)`-correct randomised algorithm with an oracle (O1)
makes at the constant weight, with truthful uniform answers,

    E|Q|  ≥  (1 − 2δ)(1 − η − η″) · 2ⁿ / ( L · V(n, r−1) ),      η″ = L V(n, r−1) / 2ⁿ .

(`η″` is the reciprocal of the main factor: the bound is `(1 − 2δ)((1 − η)/η″ − 1)`, and it has no side
condition — where `η″` is not small, the claim is trivial.  `δ ≤ ½` is needed only for that: for `δ > ½` and
`η + η″ > 1` the product of two negative factors would be a false positive bound.)

*Proof.*  Independent uniform centres.  Let `φ` have values in `[−1, 1]` and `ψ = φ − E_πφ`, so `sup ψ − inf ψ ≤ 2`.
By Lemma 2.5(iv), `G_ψ` has mean zero and changes by at most `2m_r` when one centre changes; by the
bounded-differences inequality (McDiarmid 1989)
`P(|G_ψ(c)| > τ) ≤ 2exp(−2τ²/(L(2m_r)²)) = 2exp(−τ²/(2 R m_r)) ≤ η/M`.  Since `A(w_c) ≥ 1`,
`|E_{μ_{w_c}}φ − E_πφ| ≤ |G_ψ(c)|`: outside an event of probability at most `η` the uniform answers are admissible
for all `M` observables.  By Lemma 2.5(ii) and Markov's inequality
`P(O_c ≥ R/2) ≤ C(L,2)·m_r·V(n,r−1)·2^{−n}/(R/2) ≤ η″`, and `O_c < R/2` gives
`A(w_c) ≥ 1 + R − O_c > 1 + R/2 ≥ e^ε`.  So with probability at least `1 − η − η″` the weight `w_c` is an
alternative with `ln A(w_c) > ε` for which the uniform answers are admissible.  A point lies in
`∪_j B(c_j, r−1)` with probability at most `L V(n,r−1)/2ⁿ`.  Lemma 2.3.  ∎

*Adaptive statistical queries.*  The per-seed argument of Theorem A applies verbatim, with the good
event of the seed `ω` = {`|G_ψ(c)| ≤ τ` for the queries of `ω`, and `O_c < R/2`}: for an oracle (O2) with at most `q`
queries, `R ≥ 2(e^ε − 1)` and `2 R m_r ln(2q/η) ≤ τ²`, `E|Q| ≥ (1 − η − η″ − 2δ)·2ⁿ/(L·V(n, r−1))` (no restriction on `δ` in
this form).

*Remark (homogeneous spaces) [P; added after both reviews; then read once by the second referee, who found
it correct as stated and checked it by enumeration on four graphs — `PHASE2_REVIEW_A1.md` §6].*  Lemma 2.5 and
Theorem A′ use the cube through three facts only: maxima of dips are admissible (any metric space,
Lemma 2.1); the reference is uniform; and the number of points at each distance from a point does not
depend on the point.  The last one gives `E_π e_r(d(·, c)) = m_r` for every centre, the probability
`V(r−1)/|X|` that a uniform centre has a given point in its ball (parts (ii) and the packing step), and
the fact that for independent uniform centres the law of `(d(x, c_j))_j` does not depend on `x` (part
(iv): `E_c max_j e_r(d(x, c_j))` is a constant).  Hence both statements hold verbatim, with `|X|` in
place of `2ⁿ` and `V(r−1)` the size of a ball, on every finite metric space with that property —
vertex-transitive graphs with their path metric, Hamming spaces over any alphabet, Johnson schemes.
(For a metric that is not integer-valued, `V(r−1)` is the number of points at distance less than `r`.  The
mean-zero identity is machine-checked for finite abelian groups only, `sum_tuples_sup'_bias_eq_zero`.
Corollary A′ remains a statement about the cube.)  Whether the bound is the adaptive complexity there is
open (§11, problem 5).

*Note (the first version, and what changed).*  The version of this theorem that the first referee
read and found correct (`PHASE2_REVIEW.md` §3.2; the (O2) form §3.3) had the hypotheses `L ≥ 8τ^{−2}ln(2M/η)`,
`L m_r > e^ε − 1 + τ/5` and the bound `(1 − 2δ)(1 − η − η′)·2ⁿ/(L·V(n,r−1))` with
`η′ = (5Lm_r/(2τ))·L V(n,r−1)/2ⁿ`: it compared `μ_{w_c}` with the ideal mixture `μ̃_c` of Lemma 2.5(iii) and
needed the overlaps to be small *compared with `τ`* (Markov), which in the corollary is the side
condition `h̄(λ) > γ` (at `u = 1` and `β = 0`: `γ < 0.0154`).  That statement remains true (in constants the two
are incomparable), but the condition is an artefact: by symmetry the overlaps contribute nothing to the bias on average (Lemma 2.5(iv)), and
the bounded-differences inequality controls their fluctuations together with those of the main
term.  The present form needs the overlaps to be small only compared with the excess `R` — which is the
condition that the bound is not trivial.  It was written on 2026-11-28 after the first review.  **A second
referee reviewed exactly this section** (`PHASE2_REVIEW_A1.md`; own enumeration over all tuples of centres in
118 configurations, Monte Carlo at 16–20 sites in regimes where the overlaps are 0.7 to 12.6 times the least
tolerance the hypothesis allows — the first version is void there —, the recipe of the corollary up to
`n = 2·10⁶`): the theorem, both oracle forms, Lemma 2.5(iv) and the corollary stand; it found the corner
`δ > ½`, `η + η″ > 1` in which the displayed bound was false as a statement (the first version had the same
corner; `δ ≤ ½` is now a hypothesis), five points of wording, and the sharper constant (`2` in place of `8`;
it first read the text with `8`).  All are incorporated.  The referee then read the corrected section and
the remark above once (its §6: "correct as they stand") and made four further points of wording, which
are applied too; the text after those last edits was not read again.

**Corollary A′ (exponents) [P].**  Let `τ = e^{−γn}`, `ln ln(M + 2) ≤ βn + o(n)`, `λ = 2γ + β < a`, bounded
accuracy, `δ < ½`.  Then the adaptive exponent with the oracle (O1) — and with an oracle (O2) answering
`q` adaptive statistical queries, `ln ln(q + 2) ≤ βn + o(n)` — is at least

    h̄(λ)  :=  KL(ρ₀ − λ/u ‖ ½) − λ .

`h̄` is convex and decreasing on `[0, a]`, `h̄(0) = h`, `h̄′(0) = −(1 − ℓ)`, `h̄(a) = 0 = h̄′(a)`; so
`h̄(λ) ≥ h − (1 − ℓ)λ`, against `h − λ` from Theorem A, and `h̄(λ) > 0` for every `λ < a`.  At `u = 1`:
`1 − ℓ = 0.5100`; for `β = 0` the bound is positive up to `γ = a/2 = 0.0555`, while `h − 2γ` vanishes at
`γ = h/2 = 0.01457`.

*Proof.*  It suffices to treat equality, `ln ln(M + 2) = βn + o(n)`: an algorithm may ignore observables (or
make fewer queries), so a bound for a larger family holds for every subfamily.  Fix `η < 1 − 2δ`.  Let `r` be the
largest radius with `2(2e^ε − 1)·m_r·ln(2M/η) ≤ τ²` — it exists
for large `n`, because `m_1 = (e^u − 1)2^{−n}` and `λ < a < ln 2` — and `L = ⌈2(e^ε − 1)/m_r⌉`.  Then
`m_r < 1`, `2(e^ε − 1) ≤ R ≤ 2(e^ε − 1) + m_r ≤ 2e^ε − 1`, and the hypotheses of Theorem A′ hold.  Consecutive
masses differ by a factor `e^{o(n)}`: `m_{r+1} ≤ (e^u + 1 + n)·m_r` (term by term
`e^{u(r+1−j)} − 1 ≤ (e^u + 1)(e^{u(r−j)} − 1)` for `j < r`, and the new shell has at most `n` times the points of
the last one).  Hence `m_r = e^{−λn + o(n)}`, `L = e^{λn + o(n)}`; by `n^{−1}ln m_r → u(ρ − ρ₀)` for `r/n → ρ ∈ (p_u, ½)` (§1) and the monotonicity of `m_r` in `r`,
`r/n → ρ₀ − λ/u > p_u`, and `n^{−1}ln(2ⁿ/(L V(n,r−1))) → ln 2 − λ − h₂(ρ₀ − λ/u) = h̄(λ)`; in particular
`η″ → 0`.  `h̄′(λ) = u^{−1}ln((1−ρ)/ρ) − 1` at `ρ = ρ₀ − λ/u`, which vanishes at `ρ = p_u`, i.e. at `λ = a`;
`h̄″ = 1/(u²ρ(1−ρ)) > 0`.  ∎

| `γ` (`u = 1`, `β = 0`) | Theorem A: `h − 2γ` | Corollary A′: `h̄(2γ)` | upper bound `(1 − γ/ln 2)h` (§5) |
|---|---|---|---|
| 0 | 0.029139 | 0.029139 | 0.029139 |
| 0.002 | 0.025139 | 0.027133 | 0.029055 |
| 0.005 | 0.019139 | 0.024252 | 0.028929 |
| 0.010 | 0.009139 | 0.019795 | 0.028719 |
| 0.0145 | 0.000139 | 0.016154 | 0.028530 |
| 0.020 | — | 0.012188 | 0.028298 |
| 0.030 | — | 0.006364 | 0.027878 |
| 0.040 | — | 0.002380 | 0.027458 |
| 0.050 | — | 0.000302 | 0.027037 |
| `a/2 = 0.05547` | — | 0 | 0.026807 |

The gap between the last two columns is open (§11, problem 1); beyond `γ = a/2` Theorems A and A′ give no
lower bound for randomised algorithms, while the upper bound stays positive up to `γ = ln 2`.

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
this form with product weights, `λ₁/λ₀ = (e^{−γ} − e^{−u})/(1 − e^{−(u+γ)})` per site — nonnegative iff `|γ| ≤ u`).  Then Theorem A″ holds
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
cube).  (3) **For a non-uniform reference the theorem gives a positive but smaller exponent** [P for the
limits; N for the numbers: `experiments/phase2/p2_field_flat.py`, `p2_field_flat_exact.py`; the referee's
`experiments/phase2/review/r3_field.py`].  For `π = Bernoulli(p)ⁿ` and the baseline `e^{−γ|x|}` write
`μ_{w₀} = Bernoulli(p′)ⁿ` (`logit p′ = logit p − γ`), `z₀ = e^{−(u−γ)}`, `z₁ = e^{−(u+γ)}`, `s₀ = 1 − p′ + p′z₀`,
`s₁ = p′ + (1 − p′)z₁`.  The hiding law is `Bernoulli(θ)ⁿ`, `θ = (1 − z₀)s₁/(1 − z₀z₁)`, and for every `n`, every
query and every `t ≥ 0` (Chernoff)

    P_hit  ≤  ε₀^t · max( ρ_t(0), ρ_t(1) )ⁿ ,     ρ_t(0) = θ(z₁/s₁)^t + (1−θ)s₀^{−t},   ρ_t(1) = (1−θ)(z₀/s₀)^t + θ s₁^{−t} ,

with equality at the exponential scale (Cramér): `−n^{−1}ln P_hit → max_t min_a(−ln ρ_t(a))`.  At the
constant weight and `p < ½` the worst query is the mode and the limit is `KL(κ*‖θ)`,
`κ* = ln(1/s₀)/(u + ln(s₁/s₀)) < θ`: **`0.0109` at `p = 0.3`, `u = 1` and `0.0056` at `p = 0.1`, `u = 2`** — positive, and
reached slowly (`0.0214` and `0.0153` at `n = 160`; `0.0109` and `0.0056` at `n = 10⁵`).  The best values over
`γ` are `0.0122` and `0.0106`, against the class exponents `0.0250` and `0.0481` of Theorem 11.59: **49 % and
22 %** (43 % and 12 % at the constant weight).  So with a field **a positive exponent survives every
family of `exp(e^{o(n)})` observables at sub-exponential precision** [P]; whether the class exponent
itself is invariant is open (§11, problem 4).  (Flatness is the identity `ρ₁(a) = 1`, so the flat exponent
is positive for every product reference and every `|γ| < u`; at `γ = 0`, `p < ½` the mode is the binding
query for every `u` — the referee's remarks, review §4.3.)  For one-body data with a field exact
invariance of both class exponents is known by a different mechanism (compensation; theory report
Theorem 11.109a, science division).
*Two errors of the first versions of this paragraph, found by the referee:* it said that the bound is
"void at the exponential scale at the constant baseline" — an extrapolation from `n ≤ 160`, where the
exponent is still falling; and its numbers for tilted baselines (`0.0236`, `0.0203`, "40 %–95 %") came
from a script with the reciprocal of the correct product weights, i.e. from a family that is not
flat.  (`docs/DEAD_ENDS.md`, D71.)
(4) *What is unique.*  The kernel is invertible (least eigenvalue `(1 − e^{−u})ⁿ` on the cube), so the
coefficients `q(c)H(c)` of a flat superposition of cones are forced to be constant: cones of equal
*height*.  The hiding law is not forced: every `q̃ > 0` with heights `ε₀/(Σ₀q̃(c))` is flat.  What singles
out `q ∝ m` is the normalisation "all members have the same mass" — it minimises the second moment
`ε₀²Σ_c q(c)²/q̃(c)` of the masses, which is what the concentration step pays for.  Whether unequal
masses do better with a field was not examined.

### 2.5 Dependent references: a sandwich by absorption

For an *interacting* known part the flat family has not been evaluated.  A cruder tool works for every
known part of bounded local oscillation, dependent or not.

**Proposition 2.7 (absorption) [P].**  Let `π₀` be a reference measure on the cube, `f` a *known* function
with `|f(x) − f(y)| ≤ κ·d(x, y)`, `0 ≤ κ < u`, and `π = e^{−f}π₀/Z_f`, `Z_f = E_{π₀}e^{−f}`.  Write `P(π, u)` for the
problem "`ln E_π w` for `w ∈ 𝒲_u`, by evaluations of `w`, with any oracle about the ensemble `wπ/E_π w`".  Then

    P(π₀, u − κ)   ≤   P(π, u)   ≤   P(π₀, u + κ)

in the following sense: `w ↦ w e^{−f}` maps `𝒲_u` into `𝒲_{u+κ}` and `v ↦ v e^{f}` maps `𝒲_{u−κ}` into `𝒲_u`; in both
cases the two instances have **the same ensemble**, their targets differ by the known constant `ln Z_f`,
and an evaluation of one is an evaluation of the other.  Hence every lower bound for `P(π₀, u − κ)` —
with or without an observation oracle — holds for `P(π, u)`, and every algorithm for `P(π₀, u + κ)` solves
`P(π, u)` with the same number of evaluations.

*Proof.*  `|ln(we^{−f})(x) − ln(we^{−f})(y)| ≤ (u + κ)d(x, y)`, and similarly for `ve^{f}` with `u − κ + κ`.
`E_{π₀}[we^{−f}] = Z_f·E_π w`; the ensembles `we^{−f}π₀` and `wπ` are proportional.  ∎

**Corollary 2.7 (observation invariance for dependent references, in sandwich form) [P, given the
cube theorems].**  Let `π₀` be uniform and `f` be `κ`-Lipschitz, `κ < u` — a field, a pair interaction with
`max_i (|θ_i| + Σ_j |J_{ij}|) ≤ κ`, any energy whose single-site moves cost at most `κ`.  Then for the
reference `π ∝ e^{−f}` and bounded accuracy:

    h(u − κ)  ≤  adaptive exponent  ≤  h(u + κ) ,        a(u − κ)  ≤  non-adaptive exponent  ≤  a(u + κ) ,

and **the two lower bounds persist with means of `M` arbitrary bounded observables at tolerance `τ`
whenever `ln(1/τ) = o(n)` and `ln ln M = o(n)`** (Theorem A at the slope `u − κ`), with the explicit factor
`L` of Theorem A at every `n`.  At `u = 1`, `κ = ¼`: `0.0169 ≤ … ≤ 0.0439` (`h(1) = 0.0291`).  With site-dependent
bounds `κ_i` the same holds with site-dependent slopes `u ∓ κ_i` (classes with several site types, theory
report §11.26).

*Remarks.*  (1) The sandwich is not sharp — for a field the exact class exponent is known
(Theorem 11.59) and lies strictly inside, and with observations the flat family of §2.4 does better
(`0.0109`–`0.0122` against `h(u − κ) = 0.0007` at `p = 0.3`, `u = 1`, where `κ = 0.847`; at `p = 0.1`, `u = 2` one has
`κ = 2.197 ≥ u` and the proposition does not apply at all) — but it needs no structure of `f` beyond the
bound `κ`, and it is the only statement we have that covers **interacting** known parts together with
**arbitrary** observables.  (2) It answers, in this weak form, the question the science division left open after
its Theorem 4 ("a known part that is not invariant under a large group of translations: open"), for
noisy data of every kind; for exact one-body data with a field its compensation theorem is sharp.
(3) The same absorption shows that the class is stable under *marginalisation with a dependent
reference*: integrating out a block `Z` of sites turns `𝒲_u` into `𝒲_{u+κ}` on the remaining sites, `κ` the
oscillation over `z` of the energy difference of a single-site move (THY-MSG-0023 §3).

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
(c) *The bound on `|C|` is tight up to the factor 2:* if `S = W∖{0}` for a subspace `W` of dimension
`d` (`M = 2^d − 1`), every subgroup with `C^⊥ ∩ S = ∅` has `|C| ≥ 2^d = M + 1`.  (This is about the subgroup
method; for a coordinate subspace the complexity itself is given by Theorem C.)
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
(ii) It is also obtained from the `2^b` indicator functions of the cells at tolerance `τ2^{−b−1}` (a law
consistent with the reports is within `τ` in `‖·‖₁`).  So with
`M = e^{γn}` observables at tolerance `e^{−γn − O(1)}` the exponent is at most `(1 − γ/ln 2)h`:
**`ln(1/τ) = o(n)` cannot be dropped.**  With adaptive statistical queries (O2), `2b` queries suffice
(halving: both halves are queried at each level and the heavier one is kept).
(iii) Consequently `(1 − γ/ln 2)h` is an upper bound for the exponent in the regime of Corollary A′.

**Proposition C′ (the full oracle; one exact number) [P].**
(a) Let the oracle return any `μ̂` with `‖μ̂ − μ_w‖₁ ≤ τ` (this is what all indicator functions at
tolerance `τ/4` give).  Draw `x_1, …, x_k ~ μ̂` independently and return the median of
`ln w(x_i) − n ln 2 − ln μ̂(x_i)`.  Each term is within `ε/2` of `ln A(w)` unless `|μ_w(x_i)/μ̂(x_i) − 1| > κ := 1 − e^{−ε/2}`,
which has probability at most `τ/κ`; so `k` evaluations are `(ε/2, δ)`-correct as soon as
`(4τ/κ)^{k/2} ≤ δ` (this needs `τ < κ/4`): **`O(ln(1/δ)/ln(κ/τ))` evaluations, independently of `n`**; with
`τ ≤ κδ` one evaluation suffices.
(b) One exact value `μ_w(z)` and one evaluation give `A(w) = w(z)2^{−n}/μ_w(z)` (**[K]**: the science
division's addendum A8, "the full law at one point").  So for *exact*
observables the size of the spectrum in Theorem B is the right parameter: the indicator of a point
has full spectrum.
(c) *Deterministic algorithms do not profit in the same way.*  For a deterministic algorithm with
any oracle (O1)/(O2) of tolerance `τ`, any number of observables: let it evaluate the set `Q` at the
constant weight (uniform answers), and put `ρ = ⌈Δ/u⌉ − 1`, `Δ = ε + ln 2`, `p = π(∪_{x∈Q} B(x, ρ))`.  The
weight `w = min(e^Δ, e^{u·d(·,Q)})` is admissible, equals `1` on `Q`, and has `A(w) > e^Δ(1 − p)` and
`TV(μ_w, π) ≤ p` (`w < A` only inside the balls).  If `p ≤ τ/2`, every answer given at the constant weight is
admissible for `w` and `A(w) > e^ε`, so the algorithm errs; hence `|Q| ≥ (τ/2)·2ⁿ/V(n, ρ)`.  Conversely, for
`τ ≤ κ/8`, `κ = 1 − e^{−ε/4}`, and `b = ⌊log₂(κ/(8τ))⌋`: `2b` halving queries (indicators of subcubes; both
halves are queried at each level and the one with the larger reported mass is kept) find a subcube
`T` of codimension `b` with `μ_w(T) ≥ 6τ/κ`, known to
relative accuracy `κ/6`, and a `⌊ε/(4u)⌋`-net of `T` determines `E_π[w1_T]` to within `e^{±ε/4}`:
`2^{n−b} ≤ (16τ/κ)·2ⁿ` evaluations.  **Deterministic cost with observations at tolerance `τ`: `τ·2ⁿ` up to
factors polynomial in `n`** — the tolerance buys exactly its own factor, whatever is observed.

*Reading.*  Rows A, C, C′ together: for randomised algorithms the *lower* bounds are governed by
`τ^{−2}ln M` — the number of samples of the hidden structure that the data cannot tell from the
continuum.  The value of the data is negligible while `ln(τ^{−2}ln M) = o(n)`; it is a constant fraction
of the exponent in the examples with `ln ln M` or `ln(1/τ)` of order `n` (Theorem C, Corollary C); and it is
everything when `ln ln M ≈ n ln 2` (all indicator functions, C′ (a)) or `τ ≈ 2^{−n}` (C′ (b)).  The known
upper bounds weight `ln(1/τ)` once, not twice: with cell indicators at `τ = 2^{−n/2}` the exponent is at most
`h/2`, not `0`; between the bounds the truth is open (§5).

---

## 5. The exponentially precise regime: what is known

`τ = e^{−γn}`; randomised algorithms; bounded accuracy; `u = 1` for numbers.

| observables | lower bound for the exponent | upper bound | source |
|---|---|---|---|
| any `M = e^{o(n)}` fixed, or `q = e^{o(n)}` adaptive | `h̄(2γ)` for `γ < a/2` (it exceeds `h − 2γ`); none for `γ ≥ a/2` | `(1 − γ/ln 2)h` if the family contains cell indicators | A, A′, Corollary C |
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
most `τ√η`, and it is not hidden from the character at the maximising frequency if `β(Γ)` exceeds `τ`
divided by the factor `1 − 1/A` between the excess measure and the ensemble.  The
three known constructions are the three ways of making `β` small:

| centres `Γ` | bias `ρ̃_Γ(s)` | atoms needed |
|---|---|---|
| `L` independent uniform points (Theorem A) | of size `L^{−1/2}` at every `s` | `τ^{−2}` (times `ln M` for `M` observables, by Hoeffding instead of Chebyshev) |
| a subgroup `C` (Theorem B) | the indicator of `C^⊥` | zero error for every observable whose spectrum avoids `C^⊥`: `< 2(M+1)` |
| a linear code of dual distance `k_τ = ln(1/τ)/ln(1/t)` (science division, Theorem 4-τ) | the indicator of `C^⊥`, attenuated by `t^{|s|} ≤ τ` on it | between `V(n, k_τ/2)` (Rao) and `e^{n h₂(k_τ/n)}` (Gilbert–Varshamov) |

For `τ = e^{−γn}` with small `γ` the first is the cheapest (`e^{2γn}` against `e^{n h₂(κ)}`,
`κ = γ/ln coth(u/2)`), and unions of `m` random cosets of a code of dual distance `J` cost
`V(n, J/2)·τ^{−2}t^{2J}`, which is increasing in `J` at `J = 0` (and concave on `[0, k_τ]`, so its minimum is at an end): **none of these
constructions has fewer than about `τ^{−2}` atoms at small `γ`** — a statement about the constructions,
not a lower bound for hiding families.  Whether fewer atoms can hide (a set with attenuated bias `τ` and
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
a sampled centre would reveal the scale `1/K` of an averaged dip.  (2) In terms of `m`, to first order in `ν`:
`N ≳ N₀/m^{2−ℓ}` — against `(τ^{−2}ln M)^{1−ℓ}` for means.
(3) **No algorithm is known that uses samples to beat `e^{nh}` on the whole class**
[open: §11, problem 2].  The identity `A = E_π[w·1_T]/μ_w(T)` with `T = {w ≤ θ}` costs `1/μ_w(w ≤ A)` samples, which at
the cone is again `e^{nh}` (`h` is the Chernoff information between `π` and the cone's ensemble).
With samples of *pinned* ensembles the problem is polynomial (self-reducibility; science
division, addendum A7).  (4) *Larger accuracies.*  The theorem is stated for `ε < ln(11/8)`.  For any
bounded `ε` compare `K` dips with `CK` dips, `C = ⌈2e^ε⌉`: the ratio of the partition functions is at least
`(1 + (C − ¼)R)/(1 + R) ≥ (40C − 9)/41 > e^ε` (as `R ≥ 40`), there are `(C − 1)K` extra centres, the hypothesis
becomes `N* ≥ 40C²m/η₁` and the bound `(1 − 2δ − O(η₁))N*/(C − 1)`; the exponent does not change.  (5) In the proof, `E|Q₀|` is first the cost in the coupled experiment; coupling the
coupled pair (instance, samples) maximally with the true one costs the bad-sampling probability of
experiment 0 once more, which is the term `1.55η₁` on the left of the last display.

---

## 7. A hierarchy of information operators

Cost of `ln A` to bounded accuracy on the cube class, randomised algorithms, leading exponent.

| operator | exponent | reference |
|---|---|---|
| evaluations only | `h` (adaptive), `a` (fixed sample) | theory report §§11.10–11.19 |
| + means of `M` observables at tolerance `τ`, `ln(τ^{−2}ln M) = o(n)` | unchanged | Theorem A |
| + the same with `τ = e^{−γn}`, `ln ln M ≈ βn`, `λ = 2γ + β` | at least `h̄(λ)` (`λ < a`); at most `(1 − (γ+β)/ln 2)h` for suitable families (cells of a block times unions inside a cell) | A′, C |
| evaluations (+ such means) with a known `κ`-Lipschitz energy in the reference | in `[h(u − κ), h(u + κ)]` | Proposition 2.7 |
| + exact means, joint spectrum `e^{λn}` | `≥ h̄(λ)`; `= (1 − θ)h` for the law of `θn` coordinates | B′, C |
| + exact marginals of every order `≤ αn` | in `[h̄(h₂(α)), (1 − α)h]` | Corollary B′ |
| + the mean energy (calorimetry) | `h` in the worst case | science division, Proposition 5b |
| + `e^{νn}` samples | in `[h̄(ν) − ν, h]`; total cost `≥ ν*` | Theorem E |
| + `e^{νn}` samples, evaluations only at them and at uniform points (non-adaptive) | at most `θ_na(ν)`: `a` at `ν = 0`, `h` at `ν = h`, `0` from `ν = ln cosh(u/2)` on | bridge note, Corollary F1 [P, unrefereed] |
| + means of functions of the *energy* at tolerance `e^{−γn}` | in `[θ_hint(γ), min(h, θ_na(γ))]` for `γ < ln cosh(u/2)`; `0` (a bounded number of evaluations) beyond | bridge note, Theorem J [P, unrefereed] |
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
homogeneous space; a positive exponent for product references (flat mixture) and a sandwich for
dependent ones (absorption) — not the invariance; the adaptive exponent `h̄(2γ + β)` in place of
`h − 2γ − β`, on the whole range `2γ + β < a`; the fact that neither condition can be dropped; the
collapse beyond them.  (The texts of S1 and S2 are not in the repository; what was checked is the
statements as rendered in the directive.)
**S2 — correct.**  `r = ⌈log₂(M+1)⌉` generators, a subgroup with `|C| ≤ 2^r < 2(M+1)` whose dual avoids `S`,
loss at most `|C|`.  Strengthened: arbitrary exact observables through their joint spectrum;
tightness of the bound on `|C|` up to the factor 2 for the subgroup method; the exponent `h̄(λ)`; the
sharp value for a block of coordinates.

**Against the archive** (science division, `INFERENCE_LIMITS.md` and addenda; theory report §§11.27, 11.29).

| statement here | what the archive has | what is new |
|---|---|---|
| Theorem B(d): exact marginals of order `o(n)` change no exponent | Theorem 4 with BCH codes (`k = o(n/ln n)`), addendum A1 / Proposition 11.104 (non-adaptive), Theorem 4‴ of A8 with Gilbert–Varshamov (which covers `k = o(n)` for the adaptive exponent) | **nothing in substance** — S2's corollary is theirs |
| Theorem B(a)–(c): any frequency set, any exact observables by spectrum, optimal `\|C\|` | Lemma 1 (dual distance) | the formulation by spectrum; the random-subgroup bound `2(M+1)` and its optimality |
| Corollary B′: `θ(α) ≥ h̄(h₂(α))` | `θ(α) ≥ h − h₂(α)` (A8), "the gap between the bounds is open" | the lower bound; positive range `α < 0.0234` instead of `0.0046` (`u = 1`) |
| Theorem A: arbitrary bounded observables, tolerance `τ`, both exponents | Theorem 4-τ (A10): Walsh characters of every order, `τ ≥ e^{−o(n/ln n)}`, adaptive exponent, by a code and the attenuation `tanh(u/2)^j` | arbitrary observables and the count `M`; the range `ln(1/τ) = o(n)`; the non-adaptive exponent; a different mechanism (random translates) |
| Corollary A′ | A10 remark (2): "the crossover — tolerance `e^{−γn}` — is open" | two-sided bounds in the crossover |
| Theorem A″, Lemma 2.6; Proposition 2.7 | compensation for one-body data with a field (Theorem 11.109a); "a known part that is not `C`-invariant: open" (their §4, §13 item 2) | every bounded observable and every `κ`-Lipschitz known part, interacting or not — in sandwich form (`u ∓ κ`), not sharp |
| Theorems C, C′, E | the upper bound `(1 − α)h` for marginals of order `αn` and the exact zoom behind it (A8); **one exact point probability gives `ln A` with one evaluation** (A8: "the full law at one point: 0"; A7) — Proposition C′ (b) is theirs; the remark that a sampler finds the dips (A10) | the tolerant versions; the matching (cylinder) lower bound for a block; that neither hypothesis of S1 can be dropped; the full-oracle collapse C′ (a) and its deterministic counterpart C′ (c); the sample lower bound |

**Prior art outside the programme** (from memory, and a bounded search of five queries and one abstract
recorded in `docs/phase2/PRIOR_ART.md` — read at the level of search summaries; nothing below was found
stated for free energies of Lipschitz classes).  The search adds: the cell-hiding lower bound for
log-concave normalising constants (Ge–Lee–Lu 2020); partition functions from *sampling* oracles at
chosen temperatures, with lower bounds and an adaptive/non-adaptive distinction of its own (Kolmogorov
2018; Harris–Kolmogorov; Guo–Liu–Yang–Yin–Zhang 2026) — a different access model from Theorem E; no
statistical-query lower bound for partition functions was returned.  Statistical-query learning: `O(τ^{−2}log M)`
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
| Lemmas 2.1, 2.2, 2.3, 2.6, 3.1, 3.2; the form of 2.4 used; of Lemma 2.5 (iv): the mean-zero identity (`sum_tuples_sup'_bias_eq_zero`) and the 1-Lipschitz property of a maximum (`abs_sup'_sub_sup'_le`, which gives the bounded difference with `2‖ψ‖_∞` in place of the oscillation) | **[V]** `proofs/Frontiers/ObservationInvariance.lean` (41 declarations; registered in `proofs/AxiomAudit.lean`) |
| Theorems A, A′, A″, B, B′, C, C′, E; Lemma 5.1; Proposition 2.7 | **[P]** this file.  For A, A″, B the reductions to the machine-checked lemmas are short; nothing of Lemma 2.5 (ii)–(iii), A′, B′, C, C′, E, Lemma 5.1, Proposition 2.7 is machine-checked beyond the closure of the class under maxima, the mean-zero identity of Lemma 2.5 (iv) with the 1-Lipschitz property of a maximum, and two elementary inequalities of Theorem C (b); the bounded-differences inequality used in Theorem A′ is cited (McDiarmid 1989), not formalised; the argument for adaptive statistical queries is on paper only |
| the identities and inequalities of §§2–6 listed in the script's output, on small cubes (not: the chain of Theorem A′, Theorem B′ (ii), the halving guarantee, the median bound, Theorem E beyond `ν*` — the referee simulated several of these); the exponent functions | **[N]** exact enumeration, `experiments/phase2/p2_checks.py` (37 checks) and harness block XXVIII (four tests, 27 mutations, all caught).  For the new form of Theorem A′: Lemma 2.5 (iv), the exact tails against the bounded-differences bound and the overlap step by enumeration of all tuples of centres on cubes of 4–6 sites (checks A4d–A4g; harness XXVIII.2, six mutations), and the recipe of Corollary A′ at `n = 2000, 20000, 200000` beyond the old side condition (A4h) |
| internal review | one adversarial AI referee, `docs/phase2/PHASE2_REVIEW.md`: every numbered theorem of the first version stands; two numerical claims wrong and corrected; the Lean statements say what the report says they say (its §9); it did not compile the Lean file or run the harness.  The present form of Theorem A′ / Corollary A′ was written afterwards and reviewed by a second AI referee, that section alone (`docs/phase2/PHASE2_REVIEW_A1.md`): it stands, with `δ ≤ ½` added to the statement; that referee read the corrected section and the remark on homogeneous spaces once (correct as they stand; four further wording points, applied); it did not compile the Lean file or run `p2_checks.py` or the harness |
| upper bounds | rest on the cube theorems 11.44, 11.54, 11.58 ([P], refereed internally) |
| the bridge note (`BRIDGE_NOTE.md`: Theorems F, J; Corollary F1; Propositions F2, F3) | **[P], no referee**; exact steps [V] in `proofs/Frontiers/BridgeOverlap.lean` (12 declarations); [N] `experiments/phase2/p2_bridge.py` (11 checks) and harness XXVIII.5 with 13 mutations, all caught |
| audit of the repository | `bash scripts/audit_all.sh` passed on 2026-11-28 04:20 UTC on the final code (93 Lean files, 5128 declarations on the three standard axioms, 721 headline theorems; full harness 196 tests; 645 mutations, 644 caught and one expected pass); **repeated after the bridge note, 07:24 UTC**: 94 Lean files, 5155 declarations, 729 headline theorems; 197 tests; 658 mutations, 657 caught and 1 expected pass |

## 11. Open problems

1. **The exponent at tolerance `e^{−γn}`**: between `h̄(2γ)` and `(1 − γ/ln 2)h` for `γ < a/2` (§5); for
   `a/2 ≤ γ < ln 2` there is no lower bound for randomised algorithms and the upper bound is still positive.  Equivalently:
   what is the least number of atoms of a hiding family that fools every bounded observable to
   `τ` — `τ^{−2}` (random), or fewer with structure?
2. **Samples**: is there an algorithm with samples below `e^{nh}` on the whole class?  Lower bound
   `ν* ≈ 0.40h`.  (Bridge note, Corollary F1: `e^{nh}` samples make the evaluations non-adaptive — every
   ensemble of the class overlaps the reference by at least `e^{−nh−O(log n)}` — which reaches `h` and does
   not go below it; Proposition F2: one sample costs at least `e^{n(h−o(1))}` evaluations.)
3. **Exact marginals of linear order**: `[h̄(h₂(α)), (1 − α)h]`.
4. **Non-uniform references**: close the sandwich of Proposition 2.7 — is the class exponent with a
   field (Theorem 11.59), or with an interacting known part, invariant under arbitrary bounded
   observables at sub-exponential precision?  The optimal flat family (baseline and mixture).
5. **Homogeneous spaces**: on which transitive spaces is the dip-packing bound the adaptive
   complexity?  (Then Theorem A is an invariance theorem there, as on the cube.)
6. Machine-checking the passage from the cores to the displayed bounds of Theorems A and B on the
   cube (finite `n`; needs the product measure on `X^L`), and any upper bound.
7. **Observables of the energy** (bridge note, Theorem J): the exponent at tolerance `e^{−γn}` lies in
   `[θ_hint(γ), min(h, θ_na(γ))]`; the threshold `γ* = ln cosh(u/2)` is exact, the interior is open — do
   adaptive evaluations of the truncated weight reach `θ_hint(γ)`?
8. **An independent reading of the bridge note**, which has had none.
