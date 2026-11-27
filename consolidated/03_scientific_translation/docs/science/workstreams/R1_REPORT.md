# SCI-REV-0001 — independent review of theory report §11.25 ("Slices")

**Workstream R1, Scientific Discovery Division.**  Object: `docs/THEORY_REPORT.md` §11.25, *"Slices: no known
part that is a function of the type is harder than the uniform cube; reduction of algorithms to slices"* —
Lemma 11.89, Theorem 11.90, Corollary 11.91, Theorem 11.92, Lemma 11.93, Conjecture 11.94, two remarks;
`proofs/Frontiers/SliceRefinement.lean`; the README headline (x).
**Versions.**  The review was carried out at theory commit **`5ed4072`** (lines 5792–6103).  While it was in
progress the theory division published **`89ac710`**, in which §11.25 differs in three places only: the status
line (Theorems 11.78, 11.79 "refereed 'proved' by R10", report not yet published), a note in Corollary
11.91(iii), and the remark on more than two letters (rewritten, with a *Correction*; continued in a new §11.26,
Proposition 11.103).  Every finding below says which version it refers to; statements 11.89–11.93 are identical
in both.
**Labels** (COMMON rule 6): **[V]** machine-checked, **[P]** paper proof, **[K]** known and cited, **[N]**
numerical evidence, **[C]** conjecture, **[H]** heuristic.  *Independent review* = I read and re-derived;
*independent replication* = I re-computed with my own code (all scripts in `experiments/science/ws_R1/`, written
before I opened the authors' check scripts).  Working notes with every wrong turn: `experiments/science/ws_R1/NOTES.md`.
**Where the elements of COMMON's report format are:** verdicts §1; precise statements with proofs §5; numerics §11;
prior art and search log §10; what was not settled §13; next steps §14; requests §12.  This is the first independent
referee report on the section (2026-11-25).

---

## 1. Verdicts in one paragraph

**The mathematics of §11.25 is sound; its headline is broader than its theorems.**  Lemma 11.89 is true, the
authors' six-step proof is correct, and the lemma is **not new** (Hasenclever–Scholz 2013, Proposition 8(a));
I give a four-line proof by a different route that also yields a stronger pointwise statement.  Theorem 11.90
is true; (b) and (c) are proved, (a) is proved for accuracies `e ≥ 0` but **the published argument does not cover
`e < 0`** (it then proves nothing), which Corollary 11.91 needs for its non-adaptive half — I supply the missing
step and confirm it numerically.  The inequalities of Corollary 11.91 are proved; their reading as exponents is
conditional on Theorems 11.78(b), 11.79(c), and covers **only** (i) the hinted exponent of instances that are
functions of the type, (ii) lower bounds obtainable from such instances, (iii) non-adaptive algorithms.  For
**adaptive algorithms without a hint** — the class in which the uniform cube's exponent is the small one — nothing
is proved beyond "at least as hard as the cube without a field, at most as hard as the cube is for fixed
samples" (a factor 3.8 apart at `u = 1` and vanishing accuracy); hence the README sentence *"no known part that depends on the
configuration only through one order parameter … makes certification harder than no known part at all, and an
interaction without a field changes no exponent"* is **not justified as worded**.  Theorem 11.92(a), (b) and
Lemma 11.93 are proved and replicated; 11.92(c) is a correct conditional statement that currently yields no new
exponent.  The Lean file states what the prose says it states (five elementary lemmas, standard axioms only).
The remark on three or more letters at `5ed4072` contained two false statements (the "uniform 4-ary cube" values
and "the hardest known part is a uniformly weighted sub-alphabet"); **I did not find these before the theory
division's correction reached me** — I had replicated the numbers as single-centre values and objected only to
the logic; after the notice I confirmed both corrections with my own code and found that the second statement
fails even inside the range where the old remark called it true.  No critical finding; four major, twelve minor.

| statement | verdict | basis |
|---|---|---|
| Lemma 11.89 (odds ratio) | **proved**; known in print | review of both proofs + own proof; replication (10⁷ tables, 60-digit random search, limits, channel form) |
| Theorem 11.90(a) (binary centres suffice) | **proved with a gap** (`e < 0`), repaired here | review; replication with 3–5 blocks incl. `e < 0` and `N^κ` |
| Theorem 11.90(b) (closed forms) | **proved** (imprecisions of wording: m3–m6) | review; brute force over shells and exits |
| Theorem 11.90(c) (domination), table | **proved**; a stronger form holds | review; grid 270 400 points; table to all printed digits |
| Remark (softly pinned type) | **proved** as a statement about formulas; exponents given 11.78–11.80 | review |
| Corollary 11.91, inequalities | **proved** (uses the repair of 11.90(a) at `e < 0`) | review; replication with exits of every type |
| Corollary 11.91, as advertised | **weaker than advertised** | §8 below |
| Corollary 11.91(iii) | conditional on the numerical half of Prop. 11.81(b); see U1 | scan `u ≤ 6` |
| Remark (≥ 3 letters), `5ed4072` | numbers correct as single-dip values; **two statements false** (corrected at `89ac710`) | replication; confirmation after notice |
| Remark (≥ 3 letters), `89ac710` / Prop. 11.103(d),(e) | numbers **replicated** from the formulas of Thm 11.99 (not reviewed); "harder" conditional on §11.26 | replication |
| Theorem 11.92(a),(b) | **proved**; core **[V]** | review; enumeration and simulation; Lean compiled |
| Theorem 11.92(c) | **proved, conditional**; with the slice procedures available today it yields nothing beyond Theorem 11.79(c) (m8) | review |
| Lemma 11.93 | **proved** | review; exact enumeration `n = 10` |
| Conjecture 11.94 | conjecture; (ii)'s parenthesis checked | hand check of `GameFunction` |

---

## 2. Claims examined (restated with quantifiers)

Notation of §11.23/§11.25: `K(x) = x tanh x − ln cosh x`; block profiles `μ = (λ_j, μ_j)`, `MI(μ) = h(μ̄) − Σλ_j h(μ_j)`,
`dist(ν,μ) = Σλ_j|ν_j − μ_j|`; on a slice of density `κ`: `r^κ_μ(e) = min{MI(ν) : ν̄ = κ, u·dist(ν,μ) ≤ e + MI(μ)}`,
`n^κ_μ(X) = min{MI(ν) : ν̄ = κ, MI(ν) + u·dist(ν,μ) − MI(μ) ≤ X}`, `R^κ = sup_μ r^κ_μ`, `N^κ = sup_μ n^κ_μ` (over feasible
profiles); for a centre of type `m`: `F_{m,κ}`, its Legendre transform `Ψ_{m,κ}` on `ℓ ≥ 0`, `F*_{m,κ}(t) = tΨ_{m,κ}(u) − Ψ_{m,κ}(tu)`,
`F*_c(t) = t ln cosh(u/2) − ln cosh(tu/2)`.

* **C1 (Lemma 11.89).**  ∀ positive 2×2 probability tables `P` with `ln[P₁₁P₀₀/(P₁₀P₀₁)] = 2s ≥ 0`: `I(P) ≤ K(s/2)`; equality
  iff `s = 0` or both marginals uniform.  Hypotheses used: positivity; nothing else.
* **C2 (Theorem 11.90).**  ∀ `κ ∈ (0,1)`, `u > 0`: (a) `R^κ(e)`, `N^κ(X)` equal their suprema over two-block profiles;
  (b) for every centre type `m`, closed forms for the suprema over its shells; (c) ∀ `m`, ∀ `t ∈ [0,1]`:
  `F*_{m,κ}(t) ≤ F*_c(t)`, equality for some `t ∈ (0,1)` only if `m = κ = ½`; hence `R^κ ≤ R_unif`, `N^κ ≤ θ_na^cube`.
* **C3 (Corollary 11.91).**  ∀ exchangeable `π` with continuous `φ`, ∀ landscapes `λ`, ∀ profiles `μ` of type `κ`, ∀ `e, X`:
  `r_μ(e) ≤ r^κ_μ(e + (I−λ)(κ)) ≤ R^κ(e)`, `n_μ(X) ≤ n^κ_μ(X + (I−v)(κ)) ≤ N^κ(X)`; hence `R_λ ≤ R_unif`, `N ≤ θ_na^cube`,
  `R̄_H(e) ≤ max_{t≤1}[F*_c(t) − te]` for all real `e`; equality `R_H = R_unif`, `θ_na = θ_na^cube` for symmetric convex `I`.
* **C4 (Theorem 11.92).**  ∀ `n`, ∀ exchangeable `π`, ∀ `ψ ∈ L_u`: (a) `t ↦ ln A_t(ψ)` is `u`-Lipschitz, `d_t ≥ J_t − V_n(t)`;
  (b) validity, width and refinement rule of optimistic refinement; (c) *if* every slice has bracket procedures
  with exponent `τ_κ`, *then* adaptive algorithms without a hint have exponent `≤ sup_κ τ_κ(max(ε₁,(I−v)(κ))⁻)`.
* **C5 (Lemma 11.93).**  ∀ `n, k, n_o`, ∀ `ψ`: (i) `A_k = Σ_j H(j)A_{k;j}(O)` ∀ `O`; (ii) `E_O A_{k;j}(O) = A_k` ∀ `j`; Markov and
  hypergeometric-tail consequences.
* **C6 (headline).**  README (x), report §0 table, §10 (xviii), the section title.

---

## 3. Verification method

1. **Re-derivation before reading proofs.**  I had read the proof of Lemma 11.89 while locating the statements;
   I therefore proved it by a *different* route before studying theirs (thermodynamic integration on the fibre of
   fixed marginals; §5.1).  Theorem 11.90(b), (c), the corollary's inequalities, Theorem 11.92 and Lemma 11.93 I
   derived from the statements and then compared.
2. **Replication with own code**, written from the statements (no file of `experiments/coordinator_checks/slices/`
   or of the harness was opened until my scripts existed); every inner minimum is either one-dimensional and
   exact, or sandwiched by weak duality (dual value ≤ minimum ≤ value of an exactly feasible point), or solved by
   two independent solvers.  §11.
3. **Adversarial reading of the headline** against the report's own limitation section (§8 of the report, lines
   1165–1176) and the theorems it cites.
4. **Lean**: read `SliceRefinement.lean`; compiled a verbatim copy with `#print axioms` (`lake env lean`, 18 s).
5. **Prior art**: four searches and three page fetches (log in §10); A1's finding checked at the source.

## 4. Evidence inspected

`docs/THEORY_REPORT.md` at `5ed4072`: §11.25 in full; §11.23 (Theorems 11.76–11.80, Propositions 11.81–11.82,
Conjecture 11.83) for definitions; rows G27 and (xviii) of §10; §0 table row "slices"; §8 limitations; §12 item (v).
`README.md` item (x) in both versions.  `proofs/Frontiers/SliceRefinement.lean` (153 lines), `GamePair.lean`
(`GameFunction`).  At `89ac710`: the diff of §11.25, §11.26 (Theorems 11.98–11.99 statements, Proposition 11.103),
`DEAD_ENDS.md` D52, `THY-RES-0003` §4.  After my own scripts: `experiments/coordinator_checks/slices/*` and the
headings of harness block XXI.  `docs/science/workstreams/A1_REPORT.md` §2.1.  **Not inspected:** the proofs of
Theorems 11.76, 11.78, 11.79, 11.80 (only Lemma 11.77(b), which I use, was re-derived); workstream W's proofs;
referee R10's report (not in the checkout).

---

## 5. Established findings: precise statements with proofs

### 5.1 Lemma 11.89 — a four-line proof and a stronger statement  **[P, mine; every step replicated to 60 digits]**

Let `T` be a positive 2×2 table on `{±1}²` with marginals `(p, q)` and `ω := ln[T₊₊T₋₋/(T₊₋T₋₊)]` (`ω = 2s`).

1. *The fibre.*  The positive tables with marginals `(p,q)` are `T_c(b,x) = p_b q_x + c·bx`; `ω` is strictly
   increasing in `c` with `dω/dc = S(c) := Σ_{b,x} 1/T_c(b,x)`, and `ω = 0` at `c = 0`.
2. *Thermodynamic integration.*  `dI/dc = Σ_{b,x} bx·ln T_c(b,x) = ω` (the terms with `ln p_b`, `ln q_x` and the
   constant cancel because `Σ_x x = Σ_b b = 0`).  Hence `I(T) = ∫₀^ω ω′ dω′ / S(ω′)`.
3. *AM–GM.*  With `x = T₊₊ + T₋₋ ≥ 2g₁`, `y = T₊₋ + T₋₊ ≥ 2g₂`, `g₁² = T₊₊T₋₋`, `g₂² = T₊₋T₋₊`, `x + y = 1`, `g₁/g₂ = e^{ω/2}`:
   `S = (x + y)(x/g₁² + y/g₂²) = x²/g₁² + y²/g₂² + xy(g₁⁻² + g₂⁻²) ≥ 8 + 4(g₁/g₂ + g₂/g₁) = 16 cosh²(ω/4)`,
   with equality iff `T₊₊ = T₋₋` and `T₊₋ = T₋₊`, i.e. iff both marginals are uniform.
4. `I(T) ≤ ∫₀^ω ω′ dω′/(16 cosh²(ω′/4)) = ∫₀^{J} J′ sech²J′ dJ′ = J tanh J − ln cosh J = K(s/2)` (`J = ω/4 = s/2`), with
   equality iff `ω = 0` or the fibre is the one of uniform marginals.  ∎

*Stronger than the lemma:* step 3 is a pointwise statement — **among 2×2 tables with a given odds ratio the
harmonic mean of the four cells is largest for the symmetric table** — and the lemma is its integral.  In the
variables of §11.25 (`ℓ = 2c`, `s = ω/2`; the ray of a centre `(m, κ)` *is* the fibre of marginals `(m, κ)`):

> **Curvature domination [P].**  `Ψ″_{m,κ}(s) = 4/S ≤ ¼ sech²(s/2) = Ψ_c″(s)` for all `s ≥ 0`, with equality at some
> `s > 0` iff `m = κ = ½`.  Hence `D := Ψ_c − Ψ_{m,κ}` is convex with `D(0) = D′(0) = 0`.

This gives Theorem 11.90(c) in one line (`D(tu) ≤ tD(u)` for `0 ≤ t ≤ 1` is convexity with `D(0) = 0`), without
passing through the mutual information, and more: the gap `F*_c(t) − F*_{m,κ}(t) = tD(u) − D(tu)` is nondecreasing in `u`.
*Replication:* `lemma_1189.py` block P (identities to `10⁻⁶⁰`), `thm_1190.py` "curvature domination" (4 000 random
`(m, κ, s)`: `max[Ψ″_{m,κ} − Ψ_c″] = −1.4·10⁻⁵ < 0`).

**The authors' proof [P; independent review + replication].**  I re-derived steps (1)–(6): the information
density; `∂I/∂h₁ = ½(1−μ²)[T(h₂) − δ(h₁)Δ(h₂)]`; `T < 0` on `h > 0` (both cases `b ≥ 0`, `b < 0`); the closed form of
`−T − δΔ` and its reduction to `X ln(Y/X) < (1−Y) ln((1−X)/(1−Y))` with `g_W′ < 0`; the envelope step (5); evenness.
All correct.  On step (5), which the theory division singled out: the root of `δ(h₁) = T(h₂)/Δ(h₂)` exists
because `|T/Δ| < δ(h₂) < J` — that is (4), which the text cites one line *after* asserting the maximiser — and
the maximiser is a differentiable function of `h₂` because `∂²I/∂h₁² = −½(1−μ²)δ′(h₁)Δ(h₂) < 0` there; with these two
remarks the envelope theorem applies as written.  `lemma_1189_authors_steps.py` checks all six steps in
40-digit arithmetic, including `dC/dh₂` against a finite difference of the *directly maximised* capacity.

### 5.2 Theorem 11.90(a): the gap for `e < 0`, and its repair  **[P, mine]**

*What the text proves.*  For `e ≥ 0` every profile is feasible, the dual function is linear in the law `ρ` of the
block densities, the laws with mean `κ` are mixtures of two-point laws: correct.
*What it does not.*  For `e < 0` a profile is feasible iff `E_ρ KL(·‖κ) ≥ −e`, a **second linear constraint on `ρ`**.
The decomposition into two-point laws ignores it; the two-point components can be infeasible, and for an
infeasible law `sup_{t,ξ}[E_ρ g_{t,ξ} − te] = +∞` (let `t → ∞`).  Read literally, the displayed chain gives
`R^κ(e) ≤ +∞` for every `e < 0`.  Negative accuracies are not a curiosity: Corollary 11.91 asserts
`R̄_H(e) ≤ max_t[F*_c(t) − te]` "for all real `e`", and its non-adaptive conclusion evaluates `R̄_H^{−1}(θ)` at negative
arguments (for the cube at `u = 1` and small `ε₁`: at `e ≈ −0.11`).

> **Repair.**  Let `−h(κ) ≤ e < 0` and `C_e := {ρ : E_ρ x = κ, E_ρ KL(x‖κ) ≥ −e}`.  For fixed `(t, ξ)` the supremum of the
> linear functional `ρ ↦ E_ρ g_{t,ξ}` over the laws in `C_e` with a given finite support is attained at a vertex.  A
> vertex has at most three atoms, and if it has three, both constraints are active: `MI(μ) = −e`, the budget
> `e + MI(μ)` is zero, the only exit is `ν = μ`, and `r^κ_μ(e) = −e`.  By weak duality `E_ρ g_{t,ξ} − te ≤ r^κ_μ(e)` at every
> vertex, so `R^κ(e) ≤ max(R^{κ,(2)}(e), −e)`.  Finally `R^{κ,(2)}(e) ≥ −e`: on the ray of the centre `m = κ`, `F` takes every
> value in `[0, h(κ)]`, and the shell with `F = −e` has value `−e`.  Hence `R^κ(e) = R^{κ,(2)}(e)` for all `e ≥ −h(κ)`; for
> `e < −h(κ)` no profile is feasible.  ∎

For `N^κ` and `X ≥ 0` all profiles are feasible and the published argument is complete.
*Replication:* `thm_1190a_blocks.py` — best profiles with 3, 4, 5 blocks (12 starts each) against the two-block
supremum at `e = −0.03, −0.05, −0.1`: equal to nine digits (`0.041619952`, `0.059049667`, `0.121444088`).

### 5.3 Theorem 11.90(b), (c) and the table  **[P; independent review + replication]**

(b) is a one-dimensional computation; my derivation agrees (the Lagrange multiplier `τ/(1−τ)` and the range
`s ≤ u` included).  The pair identity `N^κ(e + R^κ(e)) = R^κ(e)` needs no concavity: `N(X) = min{θ : R(X − θ) ≤ θ}` for any
`F` with `R(e) = max_t[F(t) − te]`, `F(1) = 0` and `X > 0`.  Four imprecisions are listed as minor findings m3–m6.  (c): §5.1.

### 5.4 Corollary 11.91 — what is proved, exactly  **[P; independent review]**

> **(A) Unconditional inequalities between variational functions [P].**  For every exchangeable `π` with continuous
> `φ`, every landscape `λ`, all real `e` and all `X ≥ 0`: `R_λ(e) ≤ sup_κ R^κ(e + (I−λ)(κ)) ≤ R̂_c(e)`, `N(X) ≤ θ_na^cube(X)`,
> `R̄_H ≤ R̂_c` (with §5.2 for `e < 0`).  If `I` is symmetric and convex: `R_H = R_unif` and `N = θ_na^cube` (the cube's
> optimal profile has a minimal exit of type `½`, by convexity of the feasible set and of `MI` and the reflection
> that exchanges the blocks; for `n_μ` the same argument applies to `{MI(ν) + u·dist + v(ν̄) ≤ const}`).
> **(B) Given Theorem 11.78(b)**: the hinted exponent of every instance *that is a function of the type* is at most
> the cube's hinted exponent at the same accuracy rate.
> **(C) Given Theorem 11.79(c)** (which uses 11.78(b)): the worst-case exponent of *non-adaptive* algorithms over the
> whole class `L_u` is at most the cube's non-adaptive exponent.
> **(D) Given Theorems 11.78(a), 11.79(a)** (every `n`, elementary; read, not re-derived by me): for symmetric convex
> `I` every algorithm needs `e^{nR_unif(ε₁⁺) − O(ln n)}` evaluations at the flat-histogram instance — a known part
> without a field is *at least* as hard as the cube.
> **(E) Not shown:** any upper bound below `θ_na` for adaptive algorithms without a hint; anything about instances
> that are not functions of the type, except through (C).

No circularity with §11.23: Lemma 11.89 and Theorem 11.90 use nothing from it; the corollary uses its
*definitions* and Lemma 11.77(b) for the inequalities, and its *theorems* only for the reading as exponents;
§11.23 nowhere uses §11.25.

### 5.5 Three letters and more: what replaces the comparison  **[P where marked; N otherwise]**

> **Universal ceiling [P, mine].**  (i) For every pair law of Potts form `P(b,x) ∝ α_b γ_x e^{s·1[b=x]}`, on any alphabets
> and with any marginals, `I(P) ≤ s²/8`.  (ii) For every site law `π` on any finite alphabet with the Hamming
> envelope `u`, the function `F*(t) = min_Q max_φ (1−t)D_t(π_φ‖Q)` of Theorem 11.99 satisfies `F*(t) ≤ t(1−t)u²/8`; hence
> `h = max_t F* ≤ u²/32`, `E ≤ u²/8`, `a ≤ u²/8`.  The two-letter cube attains the ceiling to leading order:
> `F*_c(t) = t(1−t)u²/8 − O(u⁴)`.

*Proof.*  (i) On the fibre of fixed marginals `dI/ds = s·dE[1_{B=X}]/ds`, and `dE[1_{B=X}]/ds` is the residual variance of
the indicator after projecting out functions of `b` alone and of `x` alone (Schur complement of the Fisher
information), at most `Var(1_{B=X}) ≤ ¼`.  (ii) Take `Q = π`: `(1−t)D_t(π_φ‖π) = tΛ(1) − Λ(t)` with `Λ(t) = ln E_π e^{−tφ}`,
`Λ″ ≤ (osc φ)²/4 = u²/4` (Hoeffding), `Λ(0) = 0`.  ∎
(ii) is conditional on Theorem 11.99 only for its *reading* as an exponent; for a general site envelope replace
`u` by `max d`.  *Replication:* `ceiling_check.py` (4 000 Potts pairs `q ≤ 6`: max ratio `0.9958`; 60 random sites:
`0.9966`, `0.9971`, `0.9920`; `h₂/(u²/32) = 0.9993, 0.9955, 0.9821, 0.9325` at `u = 0.1, 0.25, 0.5, 1`).
*Reading:* with three or more letters a known part can make certification harder than none — but never by
more than the distance of the unconstrained site from the ceiling `u²/32`: for three letters at vanishing
accuracy between `2 %` (`u = 1`) and `11 %` (`u → 0`; `h₃/(u²/32) = 0.903, 0.923, 0.950, 0.981` at `u = 0.1, 0.25, 0.5, 1`).

**A new data point [N; duality bracket `10⁻⁹`; formulas of Theorem 11.99 taken as given] (`89ac710`).**  At `u = 0.5` the
three-letter site law `π = (0.04502, 0.45679, 0.49819)` has `h ∈ [0.007675293, 0.007675295]`, **above the two-letter cube**
`h₂ = 0.007672866` (and `(0.05, 0.45, 0.5)`: `0.007675166`; `(0.001, 0.4995, 0.4995)`: `0.007672975`).  So "the hardest known
part is a uniformly weighted sub-alphabet" fails also at vanishing accuracy and for `u ≤ 0.5194`, where the
`5ed4072` remark called it true; the theory division's own counterexample (`(0.05, 0.5, 0.45)`, `u = 1`) concerns
the threshold `E`.  The excess is `0.03 %`.  (`remark_v2_extra.py`.)

### 5.6 A generalisation of the lemma to many spins  **[C; N; P for three spins]**

> **Conjecture.**  In a ferromagnetic Ising model (`J_ij ≥ 0`) with arbitrary external fields, the log odds ratio of
> the joint law of any two spins is at most its zero-field value; hence (Lemma 11.89, and uniform margins at zero
> field) **the mutual information between any two spins is largest at zero field.**

Three spins **[P]**: `ω_{uv} = 4J_{uv} + ln[(cosh 2h_w + cosh 2(J_{uw}+J_{vw}))/(cosh 2h_w + cosh 2(J_{uw}−J_{vw}))]`, decreasing in `|h_w|`,
independent of `h_u, h_v`.  **[N]** 3 000 random ferromagnets on 3–6 spins: no violation (`3·10⁻¹⁵`); with couplings
of mixed sign both statements fail (718 and 105 violations).  Related and known **[K, abstract]**: Ding–Song–Sun,
spin–spin *correlations* of ferromagnetic Ising models are maximal at zero field.  For two spins the analogue
for the φ-coefficient is one line **[P]**: `φ = sinh 2J/√((cosh 2h₁ + cosh 2J)(cosh 2h₂ + cosh 2J)) ≤ tanh J` (Yule's `Y`).
(`ising_pair_generalisation.py`.)

---

## 6. Limitations of this review

* I did not review the proofs of Theorems 11.76, 11.78, 11.79, 11.80 (§11.23) or of Theorems 11.97–11.99 (§11.26).
  Every statement about *exponents* in this report inherits their status.  One cross-check: for two letters the
  vertex-channel formula of Theorem 11.99 and a direct sup–min over binary centres with exits of every type
  give the same `0.025034` (field `p = 0.3`, `u = 1`).
* Referee R10's report is not available to me; "refereed 'proved'" for 11.78/11.79 at `89ac710` is the authors'
  statement.  One statement attributed to R10 I could not reproduce (U1).
* Numerical replication is on grids and random samples; outer maximisations are multistart local searches (a
  failure to find a counterexample is not a proof).  Two bugs of my own brute-force code and one false alarm
  occurred and are documented (§11, `NOTES.md` steps 4, 11); all three were over-estimates of an inner minimum
  or a mis-located feasible set — the failure mode the authors record in D49/D51.
* Machine load: other workstreams used the same four cores (load 10–17); grids were reduced accordingly.
* The prior-art search was short by design (A1 did the deep one).

---

## 7. Findings

### Critical
None.

### Major

**M1 — The headline is broader than Corollary 11.91.**  *(both versions)*
*Location:* README (x) (bold sentence); report §0 table, row "slices" (bold); §10 (xviii); title of §11.25;
Corollary 11.91(ii) "an interaction without a field changes no exponent"; the *Reading* paragraph.
*What is wrong:* the theory has three exponents on the cube — hinted (`R_unif`), adaptive without a hint (`= R_unif`,
Theorems 11.54/11.58), non-adaptive (`θ_na^cube`).  The corollary bounds the hinted exponent *of instances that are
functions of the type* and the non-adaptive exponent; for adaptive algorithms without a hint and an interacting
known part the only proved bounds are `R_H ≤ θ* ≤ θ_na ≤ θ_na^cube`.  At `u = 1`, vanishing accuracy: cube `θ* = 0.029139`;
antiferromagnet without a field `θ* ∈ [0.029139, 0.110944]`.  "Never harder" and "changes no exponent" are therefore
unproved for the algorithm class in which the cube is easiest, and "hardest instance" is among symmetric
instances only (the report's own O4).  The qualifiers exist — §8 of the report says so plainly, G27 is worded
correctly, the README lists the open item some lines later — but the bold sentences do not carry them.
*Why it matters:* the sentence is the one a reader will quote; a physical reading ("a known interaction never
makes certifying a free energy harder") would be drawn from it.
*Suggested correction:* see §12, T1 (replacement text).  For *fields* the unqualified statement is a theorem
(Theorem 11.64 with Proposition 11.65(b)); say so.

**M2 — Theorem 11.90(a): the duality argument does not cover negative accuracies.**  *(both versions)*
*Location:* proof of Theorem 11.90(a); used in Corollary 11.91 ("all real `e`") and through it in the
non-adaptive comparison.  *What is wrong, why it matters, correction:* §5.2.  The statement is true.

**M3 — Remark on more than two letters (`5ed4072`): two false statements; and at `5ed4072` the conclusion compared lower
bounds only.**
*Location:* `5ed4072` lines 5989–6009.  (i) "uniform `k`-ary cubes … `R₃(0) > R₄(0)` for `u < ln 6` (… `0.006552` at `u = 0.5`)":
the number is the value of single dips on letters; the uniform four-letter site has the two-letter value
`0.007673` (it is a pair of uniform bits, so every lower bound of the binary cube transfers).  (ii) "the supremum
over known parts that are functions of the composition is attained on a sub-alphabet, uniformly weighted — is
true for `u ≤ 0.5194`": false (§5.5).  (iii) At `5ed4072` "harder than no known part" compared two *lower* bounds from
sets around one centre; the report had no upper bound for the uniform ternary cube (§11.18, §11.20 remark (4)
call larger alphabets "not worked out"/"a sketch").
*Status:* (i), (ii) were corrected by the theory division at `89ac710` (D52 item 7).  **I had not found (i) or (ii)
before the correction notice reached me** (see §9 for exactly what I had); afterwards I confirmed both with own
code, and sharpened (ii).  (iii) is addressed at `89ac710` by §11.26, which is unrefereed and whose upper bounds
are "by transfer".
*Suggested correction at `89ac710`:* cite the ceiling of §5.5 next to the remark; replace "site laws close to
`(½, ½, 0)` have the two-letter values" in Proposition 11.103(d) by "…tend to the two-letter values, and some exceed
them" with the data point of §5.5; update README (x), whose parenthesis still reads "the mutual information of a
Potts pair is largest on a sub-alphabet".

**M4 — Lemma 11.89 is in print.**  *(both versions)*
*Location:* "Prior art" paragraph after the lemma; §10 row G27; §10 (xviii) "may well be folklore".
*What:* Hasenclever & Scholz, *Comparing measures of association in 2×2 probability tables*, arXiv:1302.6161,
Proposition 8(a) (found by workstream A1; statement checked by me, §10).  *Correction:* cite it; classify G27's
first sentence as known; optionally replace the six-step proof by §5.1.  Theorem 11.90 and Corollary 11.91 are
applications and are unaffected.

### Minor

Each of these is a matter of wording or bookkeeping; none changes a result.  Where no correction is written out,
the correction is the restriction or rewording that the item states.

* **m1** *(both)* Lemma 11.89, parenthesis "the capacity-achieving input of an asymmetric one leans against the
  channel's bias".  True for the tilt `h₁` of the joint law (`−h₂ < h₁* < 0`, 30/30 cases); false for the input
  distribution, which favours the more reliable symbol (`E[B] > 0` for `h₂ > 0` in 30/30 cases, as for the
  Z-channel).  Say which is meant.  (`lean_against.py`.)
* **m2** *(both)* Proof of the lemma, step (5): cite (4) for the existence of the root, and the non-degeneracy
  `δ′ > 0` for the envelope theorem (§5.1).
* **m3** *(both)* Theorem 11.90(b), "for a centre of type `m`, the suprema over its shells": correct only with
  shells `ℓ ≥ 0`.  The two-block structure `(m, 1−m)` is "one ray" through `ℓ = 0` in both directions; the half `ℓ < 0`
  consists of the shells of the antipodal centre `1 − m` (verified: brute force over `ℓ ≤ 0` equals `V_{1−m,κ}` to
  `2·10⁻¹⁶`).  Taken over the whole ray the closed form is false (`0.1439` against `0.0201` at `(m, κ, u) = (0.83, 0.166, 4)`).  **[Note added at checkpoint 38: the two numbers are `0.1441` and `0.0202` (`0.144080`, `0.020200`) — the theory division's revised text has them right; workstream R9.]**
  Harmless after the supremum over `m`.
* **m4** *(both)* "the game form of `V` holds for all real `e`": only for `e ≥ −F_{m,κ}(ℓ_max)`; below, no shell of that
  centre is feasible, and `R^κ(e)` is a supremum over the empty set for `e < −h(κ)`.
* **m5** *(both)* "`R_unif(e) = KL((Λ₁+e)/u‖½) = max_{0≤t≤1}[F*_c(t) − te]`": the two expressions agree for `e ≥ −K(u/2)` only;
  below, the game form is `−e` and the `KL` form is larger (undefined below `−Λ₁`).
* **m6** *(both)* "strict inequality for `κ ≠ ½` wherever the right side is positive": false for `e ≤ −K(u/2)` in the
  game form (both sides equal `−e`); true for `e > −K(u/2)`.
* **m7** *(both)* Theorem 11.92(b): the cost bound omits the `n + 1` initial evaluations; the failure probability
  presupposes deterministic level-0 brackets and fresh randomness per request; the paper's lower end is
  `max_t p_tL_t`, the Lean statement's `p_kL_k` (both valid; `lower_end_any` in my copy).
* **m8** *(both)* Theorem 11.92(c) should state what it yields today: with the only bracket procedures available
  for slices (fixed samples, exponent `N^κ` given Theorems 11.79–11.80) it gives `sup_κ N^κ(max(ε₁, (I−v)(κ)))`, which
  equals `θ_na^cube(ε₁)` whenever `½` is a contact type — no gain over Theorem 11.79(c).
* **m9** *(both)* Conjecture 11.94: "What is missing for a proof of (iii) is written work, not an idea" cannot be
  checked and should be dropped or supported; the *Reading* paragraph ("each value is at most as hard as the
  unconstrained system at half filling") is proved for the hinted and non-adaptive slice functions only.
* **m10** *(both)* Lemma 11.93 ends, before the `∎`, with an unproved sentence ("With a fixed partition this is
  false …"); mark it as a remark.
* **m11** *(both)* Table of Theorem 11.90: the centre type that attains `N^κ(0⁺)` differs from the one printed (which is
  for `R^κ(0)`): `0.471, 0.442, 0.383, 0.325, 0.266` for `κ = 0.45, …, 0.1` at `u = 1`.  `N^κ` has a square-root cusp at `X = 0`
  (`N(10⁻¹²) = N(0) − 5.8·10⁻⁷` at `κ = 0.3`), so "`0⁺`" must not be evaluated at a small positive `X`
  (`out_slice_check1.txt`(e) of the authors shows `0.110924` for that reason; the table itself is right).
* **m12** *(both)* Status line "each step checked numerically": the authors' check scripts and harness XXI.2 test
  multi-block profiles for `r` at `e ≥ 0` only — not at `e < 0` (where the proof has its gap) and not for `n`.  Both are
  covered here.

---

## 8. The gap between theorem and headline (brief item 3)

| question | answer |
|---|---|
| Which exponents? | Two of three: the hinted exponent `R_λ` of instances that are functions of the type (largest: `R_H`), and the non-adaptive exponent `θ_na` of the class.  Not the adaptive exponent without a hint. |
| Which algorithm classes? | (i) algorithms that are told the instance, at symmetric instances; (ii) fixed samples, worst case over all instances of `L_u`.  For fields also (iii) adaptive without a hint (Theorem 11.64, Proposition 11.65(b), refereed). |
| Which accuracies? | `ε = ε₁n`, `ε₁ > 0`, at continuity points, and limits `ε₁ ↓ 0` of the exponent functions.  Nothing at bounded accuracy `ε = O(1)` (where §11.19 treats the cube only). |
| Which inputs? | The inequalities: none.  "Hinted exponent ≤ cube's": Theorem 11.78(b) (isoperimetry for the type-uniform measure).  "Non-adaptive exponent ≤ cube's": Theorem 11.79(c), which uses 11.78(b).  Unrefereed at `5ed4072`; "refereed 'proved' by R10" at `89ac710`, report unpublished.  The equalities' "≥" halves need only the every-`n` lower bounds 11.78(a), 11.79(a). |
| "Harder" for all instances? | No.  Among symmetric instances.  For non-symmetric instances only the non-adaptive (class-level) statement applies; whether `H` is the hardest of all instances is the report's open problem O4. |
| Circularity with §11.23? | None (§5.4). |
| What is unconditional? | (A) of §5.4; and (D): without a field, at least as hard as the cube. |

---

## 9. The remark on more than two letters: what I had found, and when (coordinator's item (ii))

*Before the notice* (`NOTES.md` step 7, `potts_three_letters.py`): (1) all numbers of the `5ed4072` remark replicated — the
crossings `s = 0.519366`, `1.335309`; maximisation over both marginals for `q = 3, 4, 5`; `R_k(0)` at `u = 0.5, 1`; the exact
crossings `u = ln 2`, `ln 6`; mismatch fractions `2 − log₂3`, `log₂3 − 1` — **as values of the single-centre formula**
(my script computes them as "single-centre shells"); (2) the objection M3(iii) that "harder" compared lower
bounds; (3) a second-order criterion (the best direction of a block maximises `‖v‖₁²/‖v‖₂²` over zero-sum `v`) that I
applied to three letters only, where it confirms `1/9 < 1/8`.  **I had not noticed that the same criterion at `q = 4`
gives `v = (1, 1, −1, −1)` with the binary coefficient `1/8`, i.e. that the `k = 4` numbers were not those of the uniform
four-letter site, nor that the sub-alphabet statement fails.**  This is not an independent discovery.
*After the notice* (`remark_v2_sites.py`, `remark_v2_extra.py`; version `89ac710`; formulas of Theorem 11.99 taken as
given, every optimum with a duality bracket `≤ 1.2·10⁻⁸`): thresholds at `u = 1`: `0.119499` (uniform three letters),
`0.120196` (`(0.05, 0.5, 0.45)`), `0.120115` (two letters) ✓; uniform sites `q = 3, 4`, `u ∈ {0.5, 1, 2, 3}`: `E`, `a`, `h` equal the best
equal grouping in all eight cases ✓ (`q = 4`, `u = 1`: `E = E₂ = 0.120115`, `a = a₄ = 0.117993`, `h = h₂ = 0.029139`; `q = 4`, `u = 0.5`:
`h = 0.007673`, not `0.006552`) ✓; laws `((1−d)/2, (1−d)/2, d)` at `u = 0.5`: `h = 0.007425, 0.007610, 0.007673` for `d = ⅓, 0.1, 0.01` ✓;
`a₂(0.3) = 0.011125`, `a₃(0.3) = 0.010582` ✓; `h_k = h_{k+1}` at `e^u = k(k−1)` for `k = 2, …, 5` ✓; on the grid of 171 laws the
uniform law is the hardest for `h` at `u = 1` (`0.030654` against `0.030572`) and `u = 2` (`0.117699` against `0.117413`) ✓ and
not at `u = 0.5` ✓.  New: §5.5.
*Assessment of the remark at `89ac710`.*  Its sentences are now consistent with Proposition 11.103(d), (e).  Its
conclusion — "with three letters a known part that pins the composition onto two of them, or a field that
nearly removes a letter, makes certification harder than no known part at small slopes" — is **[N]/[P] given
§11.26**: it needs the uniform three-letter site's exponent to *be* `h₃` (Theorem 11.98 and the numerical statement
that single-letter dips are its optimal labels), which no referee has seen.  "Exactly for `u < ln 2`" is exact for
the comparison `h₂` against `h₃`; it is not the threshold for "some known part is harder", which by §5.5 holds
wherever the unconstrained site is below the ceiling and is not characterised.

---

## 10. Originality of Lemma 11.89 (brief item 5)

**Verdict: known.**  **[K]** Hasenclever & Scholz, arXiv:1302.6161, Proposition 8: "For all `x ∈ ℝ∖{0}`: a) `sMutInf_x` has
exactly one maximum at the origin `(y, z) = (0, 0)`. b) `lim_{‖(y,z)‖→∞} sMutInf_x = 0`", with `x = ln√(p₀₀p₁₁/(p₀₁p₁₀))` (half the
log odds ratio), `(y, z)` the margin coordinates, origin = uniform margins, `sMutInf = sign(D)·`mutual information.
*Comparison of statements:* same objects (positive 2×2 tables), same constraint (fixed odds ratio `≠ 1`), same
conclusion with the equality case; (a) and (b) together give the global bound.  Their proof (two one-parameter
families that keep the odds ratio, sign of the derivative) is, according to the fetch tool's summary, sketched
("after some calculations"); A1 completed it.  *Reading level:* arXiv abstract page **[abstract]**; the ar5iv HTML full text
**[full text, read through the fetch tool, which returned the quoted proposition and a summary of the proof — I did
not read the source line by line]**.  The journal reference (Open Statistics & Probability Journal 7 (2016) 20–35,
Bentham Open, article TOSPJ-7-20) is confirmed only at the level of a **[search snippet]**; the arXiv page lists none.
*What I did not find in print:* the capacity phrasing ("among binary channels with a given odds ratio the
symmetric one has the largest capacity"); the harmonic-mean form of §5.1; Theorem 11.90.  "Not found", not "new".
*Related:* Ding, Song, Sun, arXiv:2107.09243 **[abstract]** (correlations in ferromagnets are maximal at zero field) —
the covariance analogue on any graph.
*Three proofs now exist:* the report's (capacity decreasing in the channel field, six steps), A1's (two tilts,
concavity of `ln`), and §5.1 (thermodynamic integration + AM–GM), which is the shortest and is the only one that
gives the curvature form used in Theorem 11.90(c).

*Search log.*
| # | query / URL | result | read |
|---|---|---|---|
| 1 | `arxiv.org/abs/1302.6161` | title, authors, submitted 22 Feb 2013, no journal ref on the page | abstract page |
| 2 | `ar5iv.labs.arxiv.org/html/1302.6161` | Proposition 8(a), (b) quoted; coordinates; proof sketched | full text via fetch tool |
| 3 | "mutual information of 2x2 contingency table maximal for fixed odds ratio uniform marginals standardized table" | Hasenclever–Scholz (twice); Williams, arXiv:2203.08089 (canonical table); nothing else relevant | search snippets |
| 4 | "mutual information two Ising spins coupling J arbitrary external fields upper bound … maximized at zero field" | Ding–Song–Sun 2107.09243; no formula for the mutual information | snippets; abstract of 2107.09243 |
| 5 | "binary asymmetric channel capacity odds ratio fixed, symmetric channel has largest capacity …" | nothing relevant (Z-channel pages) | snippets |
| 6 | "Hasenclever Scholz Comparing measures of association in 2x2 probability tables Open Statistics & Probability Journal 2016" | Bentham Open TOSPJ-7-20: vol. 7 (2016), pp. 20–35 | snippets |

---

## 11. Reproduction status (numerics; all in `experiments/science/ws_R1/`, `python3 <script>`; numpy, scipy, mpmath)

| script → output | what was re-computed (independent replication unless marked) | result | time |
|---|---|---|---|
| `lemma_1189.py` → `out_lemma_1189.txt` | Lemma 11.89: 9 938 940 tables (407×407 marginals incl. `10⁻⁹`, `0.499`, `0.5`, `0.501`; 60 values `s ∈ [10⁻⁴, 12]`); 19 998 random tables in 60-digit arithmetic in six regimes (odds → 1, → ∞, marginals → 0, near-uniform, coinciding cells); limits (`I/K → 16p(1−p)q(1−q)` as `s → 0`; `s = 200` at 700 digits; marginals to `10⁻³⁰`); 2 688 asymmetric channels (closed-form capacity = numerical to `4·10⁻¹³`); steps of §5.1; Hessian at the equality case | no violation; `max I/K = 1 + 1.4·10⁻¹²` at the uniform table (rounding); random search worst `(I−K)/K = −1.5·10⁻²¹` | 20 s |
| `lemma_1189_authors_steps.py` | the six steps of the authors' proof, 40 digits, 400 + 60 cases | all hold | 6 s |
| `lean_against.py` | optimal input of 30 asymmetric channels | finding m1 | 2 s |
| `thm_1190.py` → `out_thm_1190.txt` | Thm 11.90(b): 24 centres, brute force over shells with exits free on the ray, `e ≥ 0` and 70 negative accuracies, `X ≥ 0`; (c): 270 400 grid points, equality case; table `u = 1, 2`; `sup_m` domination | `\|V_brute − V_closed\| ≤ 1.2·10⁻¹⁶`; `\|V_brute − V_game\| ≤ 2.8·10⁻⁹`; `\|N_brute − N_closed\| ≤ 6.1·10⁻⁸`; min gap `6.2·10⁻¹⁰ > 0`; near `(½,½)` the gap is quadratic (`0.144, 0.144, 0.077, 0.210` per unit `dm² + dκ²` along `m`, `κ`, diagonal, antidiagonal; `u = 1`, `t = ½`); **all six table rows to the printed digits** | 5 min |
| `thm_1190a_blocks.py`, `thm_1190a_x0_check.py` | Thm 11.90(a): 150 random profiles (KKT solver against SLSQP: `7·10⁻¹⁴`; duality gap `2·10⁻¹⁶`); 11 configurations × 3, 4, 5 blocks × 12 starts, for `r` (`e ≥ 0`, `e < 0`) and `n` | best `k`-block value = two-block supremum to 9 digits; the one flagged cell (`n` at `X = 0`, `+6·10⁻⁹`) is the degenerate accuracy (excess `≤ 1.5·10⁻¹³` at `X = 10⁻⁸ … 10⁻⁴`) | 12 min |
| `corollary_1191_checks.py` → `out_corollary_1191_checks.txt` | Cor 11.91 with exits of **every** type: chain on 142 random two-block profiles over 4 rate functions (a field, Curie–Weiss with two phases, an antiferromagnet, a ferromagnet in a field) and 2 landscapes (`v`, `0`); "what the corollary does not say"; equality (ii); junction | chain `≤ 1.6·10⁻¹⁶`; field `p = 0.3`: **`0.025034`** by direct sup–min *and* by the vertex-channel formula, slice bound **`0.029139`**; Curie–Weiss `βJ = 1.5` barrier shell **`0.0251012`** (local maximum in the shell radius); equality (ii) to `3·10⁻¹⁴` | ≈ 25 min under load |
| `junction_scan.py`, `junction_exits.py` | Cor 11.91(iii): `u ∈ {1, 2, 3, 4, 6}`, `e ∈ {0, 0.3Ψ_c(u)}`, five couplings below `βJ*` | equality with the cube in all 50 cases; see U1 | 3 min |
| `potts_three_letters.py` | remark at `5ed4072` (§9) + exact finite-`n` sums: balls in the binary slice `½` certify `0.008658 / 0.007835 / 0.007694 / 0.007676`·`n` against `0.008425 / 0.007575 / 0.007446 / 0.007428`·`n` for the ternary cube (`n = 2·10³ … 2·10⁶`, `u = 0.5`, `ε = 1`) | all numbers reproduced | 3 min |
| `remark_v2_sites.py`, `remark_v2_extra.py` | remark at `89ac710`, Prop. 11.103(d), (e) (§9); new data point (§5.5) | all numbers reproduced | ≈ 35 min under load |
| `ceiling_check.py` | §5.5 ceiling; slice pair identity (`2·10⁻¹⁶`) | holds | 40 s |
| `thm_1192_1193_enum.py` | Thm 11.92(a) (`n = 6, 8`; 120 cases), (b) (3 600 runs, four bracket placements incl. adversarial), Lemma 11.93 (`n = 10`, all 252 sets `O`) | all hold to `10⁻¹⁵`; 0 violations | 4 s |
| `ising_pair_generalisation.py` | §5.6 | 0 / 3 000 violations (ferromagnetic) | 6 s |
| `SliceRefinement_copy_axioms.lean` → `out_lean_slice_refinement.txt` | verbatim copy + `#print axioms` + two additions | compiles; `[propext, Classical.choice, Quot.sound]` only | 18 s |

*My own errors on the way* (rule: never hide them).  (1) A cancellation in the discriminant of the table with
given marginals at large odds ratios (rewritten as a sum of non-negative terms).  (2) Brute force over the
whole ray instead of `ℓ ≥ 0` → finding m3.  (3) For `X = 0` a root finder returned the shell itself as the end of
the feasible interval.  (4) A two-dimensional inner solver that returned `MI(μ)` when no grid point was feasible
produced two apparent violations of Corollary 11.91 (`1.9·10⁻⁶`, and `1.2·10⁻⁴` with a "sharper" variant);
`corollary_1191_c1_false_alarm.py` exhibits a feasible exit below; solver rewritten.  (2)–(4) are over-estimated
inner minima — the authors' D49/D51 lesson, here producing a false refutation instead of a false confirmation.

**Formalisation match (brief item 4).**  `SliceRefinement.lean` **[V]**: `sum_mem_bracket` (if `L ≤ A ≤ U`, `p, A ≥ 0`, `k`
maximises `pU`: `p_kL_k ≤ Σ p_tA_t ≤ card·p_kU_k`), `bracket_width`, `argmax_deficit_le` (if `U_k ≤ c·A_k`: `p_jA_j ≤ c·p_kA_k` ∀ `j`),
`deficit_ge` (multiplicative form of `d_t ≥ J_t − V_n(t)`; I checked the passage to logarithms), `mean_le_of_biregular` (the
double counting).  They say what the prose says; hypotheses are jointly satisfiable (example compiled);
quantifier order is as in the text; no `sorry`, no extra axiom.  **Not formalised** — and the file, the index row
and the theorem header all say so: that adjacent type classes form a biregular graph; the procedure (loop,
termination, intersection of brackets); the failure probability; the cost bound; (c).  "The deterministic core
of (b)" is an accurate description; nothing about exponents is machine-checked in this section.

---

## 12. Recommended corrective action (requests to the theory division, sendable as they are)

* **T1 (M1).**  Replace the bold sentence of README (x), of the §0 table row and of §10 (xviii) by: *"Hence, for
  fixed samples, and for algorithms that are told the instance when the instance is a function of the order
  parameter, no known part that depends on the configuration only through one order parameter — ferromagnetic
  or antiferromagnetic, with any number of phases — has a larger exponent than no known part at all, and without
  a field these two exponents are the uniform cube's (given Theorems 11.78, 11.79).  For adaptive algorithms
  without a hint this is Conjecture 11.94: what is proved is that such a known part is at least as hard as the
  cube when there is no field, and at most as hard as the cube is for fixed samples; for a field it is Theorem
  11.64 with Proposition 11.65(b)."*  Retitle §11.25 accordingly; in Corollary 11.91(ii) write "changes neither the
  hinted exponent of `H` nor the non-adaptive exponent".
* **T2 (M2).**  Insert the repair of §5.2 into the proof of Theorem 11.90(a); restrict "all real `e`" to `e ≥ −h(κ)`.
* **T3 (M4, §5.1).**  Cite Hasenclever–Scholz for Lemma 11.89; state the curvature form `Ψ″_{m,κ} ≤ Ψ_c″` and use it
  for Theorem 11.90(c).
* **T4.**  Minor findings m1–m12.
* **T5 (M3, §5.5).**  Add the ceiling `F* ≤ t(1−t)u²/8` to §11.26; re-compute with your solver `h` at `u = 0.5` for
  `π = (0.04502, 0.45679, 0.49819)` (mine: `0.0076753` against `h₂ = 0.0076729`) and amend Proposition 11.103(d).
* **T6 (U1).**  Publish referee R10's report, and one concrete triple `(u, e, βJ)` with `βJ < βJ*(e, u)` at which
  `R_H < R_unif`, with the exit that achieves it.
* **T7.**  Before attempting Conjecture 11.94(iii) in general, settle the middle slice `κ = ½` (where `R^½ = R_unif`): it
  alone decides whether M1 is a matter of wording or of substance for interactions without a field.

*Request to the engineering division.*  **E1.**  *Motivation:* an empirical test of Conjecture 11.94(iii) on the
slice `κ = ½`.  *Formulation:* implement one level of the nested algorithm with a uniformly random split (Lemma
11.93) and optimistic refinement over type pairs (Theorem 11.92(b)), with the two-sample inner bracket of
Theorem 11.52, on `T_{n/2} ⊂ Q_n`; instances: planted dips `max_{y∉D}[−u·d(·,y)]` around binary centres of type `½` at
the shells of Theorem 11.90(b), and the zero residual.  *Inputs:* `n ∈ {24, 32, 40, 48}`, `u = 1`, `ε₁ ∈ {0.02, 0.05}`, `δ = 0.1`.
*Outputs:* evaluations used, validity of the bracket, against the same algorithm on `Q_n`.  *Validation:* exact
`A_{n/2}` by enumeration for `n ≤ 32`.  *Stopping:* a slice cost exceeding the cube's by more than a polynomial
factor at two consecutive `n` is a result; so is agreement.  *Resources:* minutes per instance.

---

## 13. Unresolved questions (what I did not settle)

* **U1 — Corollary 11.91(iii) and the junction.**  The `89ac710` text attributes to referee R10 that "for larger
  slopes [the junction] comes earlier" than `βJ*` of Proposition 11.81(b).  I do **not** reproduce this: at the cube's
  optimal profile, with exits of every type (grid `1001²`, quadrant-wise polishing, zooms), `r_μ(e) = R_unif(e)` to
  `3·10⁻¹³` for `u ∈ {1, 2, 3, 4, 6}`, `e ∈ {0, 0.3Ψ_c(u)}` and couplings up to 97 % of the way to `βJ*`; just above `βJ*` the value
  drops (`u = 3`, `βJ = 2.17`: `−3.0·10⁻⁴`), and the table of exits by type shows no feasible exit below `R_unif` at
  `(u, βJ) = (3, 2.0), (6, 5.0), (2.5, 1.7)`.  Either R10's statement concerns other parameters, or one of the two
  computations is wrong.  I have not seen R10's report.  **[N]**
* The adaptive exponent on a slice (Conjecture 11.94(iii)); I have no evidence either way.
* Whether the hinted exponent of a *non-symmetric* instance can exceed `R_H` (O4).
* Theorems 11.78(b), 11.79(c), 11.98, 11.99: not reviewed.
* The supremum of `h` over three-letter site laws at small slopes (§5.5 gives a lower bound and the ceiling).
* §5.6: a proof for more than three spins; its relation to Ding–Song–Sun.
* Uniqueness of the maximising profile among *multi-block* profiles in Theorem 11.90 (used implicitly when one
  says that only the cube's profile can attain `R_unif`).

## 14. The three most promising next steps

1. **The middle slice.**  Prove or refute `θ*(T_{n/2}) = R_unif` for adaptive algorithms without a hint.  It turns the
   headline into a theorem for every interaction without a field, or shows that it is false.
2. **The extremal site law.**  Determine `sup_π F*_π(t)` for the Hamming envelope on `q` letters (a Rényi-capacity
   problem by Theorem 11.99) between the lower bounds of §5.5 and the ceiling `t(1−t)u²/8`; this replaces the
   retracted "sub-alphabet" statement by a theorem and bounds how much harder a known part can make things.
3. **Zero field maximises pairwise information in ferromagnets** (§5.6): would extend "a field always helps" from
   the Curie–Weiss family towards known parts with spatial structure, where the report has nothing.

## 15. Summary of labels for the statements made here

**[V]**: the five declarations of `SliceRefinement.lean` (re-compiled).  **[P]** (mine, checked numerically): §5.1
(proof of Lemma 11.89; curvature domination), §5.2 (repair of 11.90(a)), §5.4(A), §5.5 (ceiling), the three-spin
case and the φ-coefficient bound of §5.6.  **[P]** (authors', reviewed and replicated): Lemma 11.89, Theorem 11.90,
the inequalities of Corollary 11.91, Theorem 11.92, Lemma 11.93.  **[K]**: Lemma 11.89 = Hasenclever–Scholz
Prop. 8(a) (reading level in §10).  **[N]**: the three-letter data point; U1; the many-spin conjecture's evidence.
**[C]**: §5.6; Conjecture 11.94.  All guarantees are model-relative (an idealised Hamming–Lipschitz class, known
density of states); no statement here is a physical claim.
