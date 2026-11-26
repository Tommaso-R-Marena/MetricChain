# R5 — Independent review SCI-REV-0005: theory report §11.26, Theorem 11.99 (the site function is a Rényi capacity; the dictionary with channel coding) and Theorem 11.101 (the adaptive exponent for several site types and any alphabets, a proof by transfer)

*Workstream R5 of the Scientific Discovery Division; answers item A1 of THY-REQ-0011.  Object under review: the theory
branch at commit `89ac710`, read in the read-only checkout `thy_ro`
(`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro`): `docs/THEORY_REPORT.md`
§11.26 (lines 6138–6417), `docs/workstreams/W_REPORT.md`, `proofs/Frontiers/RenyiCentre.lean`,
`docs/collaboration/messages/theory/THY-MSG-0011.md`.  Everything of mine is in `experiments/science/ws_R5/` (scripts,
outputs `out/`, running log `NOTES.md`).  Nothing was changed outside that directory and this file; no state-changing git
command; no `lake build`.*

Labels: **[V]** machine-checked (Lean declaration named), **[P]** paper proof (whose, and whether I re-derived it),
**[K]** known and cited (with reading level), **[N]** numerical, **[C]** conjecture, **[H]** heuristic.  "Review" = I
read and re-derived; "replication" = I re-computed with my own code (`r5lib.py`, written from the statements before I
opened the authors' `wv_lib.py`).

---

## 1. Verdicts

**Theorem 11.99 — proved.**  The identity `F*_j(t) = max_M −t ln Σ_a(Σ_φ M(φ)π_φ(a)^t)^{1/t} = min_Q max_φ (1−t)D_t(π_φ‖Q) = (1−t)C_t`
is correct with the conventions of §4.1 (Rényi divergence `D_t(P‖Q) = (t−1)^{-1} ln ΣP^tQ^{1−t}`, natural logarithms; the
programme is `(1−t)` × **Sibson's** information maximised over the input law; the capacity is the Rényi radius).  I
re-derived it independently (review), confirmed it by three numerically independent routes on 56 site/slope pairs to
`≤ 10⁻¹²` (replication), and compiled the Lean file.  The dictionary (`F* = t·E_0((1−t)/t)`, `R̂ = max_ρ(E_0 − e)/(1+ρ)`,
`θ_na = E_sp^{-1}`, the shear law) is pure algebra that needs no concavity; its *operational* content is exactly that of
Theorems 11.98(d) and 11.101.  No critical or major error; minor findings only (the range of `θ` in the headline
sentence, one garbled sentence, the convention "maximised `E_0`", wording).
**Theorem 11.101 — (a) proved; (b) proved with gaps.**  (a) (every algorithm, every `n`) is a correct paper step on top
of machine-checked inequalities; I re-derived it and brute-forced it with two site types and two asymmetric envelopes.
(b) (the adaptive exponent `R̂(ε₁)`; a proof by transfer): **every changed step is true and each argument can be
completed** — I went through the isoperimetric input (Lemma T′, the evaluation lemma, the window step, the six steps) line
by line, tested its single-letter core with a primal solver, and re-derived validity, width and the union bound of the
nested algorithm in the new setting.  The gaps are in what is written: (M1) the isoperimetric input in the form the
nested algorithm needs (flat-histogram reference, uniform in the composition) is stated and proved only in the
workstream report (its Theorem W2(c)), not in the theory report; (M2) "families of procedures indexed by compositions"
and their exponent functions are not defined, and the uniformity in the composition on which the level induction rests
is asserted in a parenthesis — I give the missing definition and a six-line argument (§4.6).  As in the two-letter
case the accounting of the one-level algorithm (Theorem 11.52) is inherited, nothing was simulated, and the statement
is an existence statement about exponents at extensive accuracy.  Nothing is false; nothing is weaker than the theorem
texts say; the **headlines** (README, THY-MSG-0011) are slightly stronger than the theorems in two places (§4.8, m1, m3).
All reference numbers were replicated (largest deviation `5·10⁻⁷`, the rounding of the published table), including
"fails beyond two letters" (non-concave site function, a harder non-uniform site law, the exact crossings
`e^u = k(k−1)`); one published number is off in its second digit (slope jump `+0.0052`, mine `+0.0056`).

---

## 2. Claim examined

Setting (theirs): sites `i = 1..n` of types `τ(i) ∈ {1..m}`, fractions `λ_j`; type `j` has an alphabet of `q_j` letters,
a site law `π_j` of full support and a site envelope `d_j ≥ 0` (zero diagonal, triangle inequality, **not necessarily
symmetric**); `π = ⊗π_{τ(i)}`, `d(x,y) = Σ_i d_{τ(i)}(x_i,y_i)`, class `𝒞 = {ψ : ψ(x) − ψ(y) ≤ d(x,y)}`, target
`ln E_π e^{−ψ}` to accuracy `ε₁n`, cost = evaluations of `ψ`.  `L_j = {γ : γ(a) − γ(b) ≤ d_j(a,b)}`, `𝒱_j` its vertices
modulo constants, `π_γ ∝ π_j e^{−γ}`; the game `K(a,φ) = (π_φ(a)/π_γ(a))^t` (sampler mixes letters, adversary mixes
vertices), `F_j(γ,t) = −ln val(K)`, `F*_j = max_{γ∈L_j} F_j(γ,·)`, `F* = Σ_jλ_jF*_j`, `R̂(e) = max_{0≤t≤1}[F*(t) − te]`,
`S(e) = e + R̂(e)`, `θ_na = R̂∘S^{-1}`.

* **Theorem 11.99**: the identity above; the hardest additive instance at slope `t` has the Rényi centre as Gibbs law;
  `a_j` = Shannon capacity, `E_j = min_Q max_φ KL(Q‖π_φ)`; with `E_0(ρ) = ρΣ_jλ_jC_{1/(1+ρ)}` and
  `E_sp(θ) = sup_ρ[E_0(ρ) − ρθ]`: `F*(t) = tE_0((1−t)/t)`, `R̂(e) = max_ρ(E_0(ρ) − e)/(1+ρ)`, `θ_na = E_sp^{-1}`, `E = E_sp(0⁺)`,
  `a` = capacity; "a fixed sample of `e^{nθ}` evaluations certifies the accuracy rate `E_sp(θ)`; an adaptive algorithm, or
  one with a hint, certifies `E_sp(θ) − θ`"; the uniform cube is the binary symmetric channel with crossover `1/(1+e^u)`.
* **Theorem 11.101**: (a) every algorithm makes at least `(1−2δ)exp(−tε + nΣ_jλ_jF_j(γ_j,t))` evaluations at the additive
  instance `γ`, every `n`, every `t ≥ 0`; (b) along chains with compositions tending to `λ` and for `0 < ε₁ < E` the least
  worst-case cost of adaptive algorithms without a hint is `exp(nR̂(ε₁) + o(n))`, non-adaptive ones need
  `exp(nθ_na(ε₁) + o(n))`.  Status claimed: lower bound P from machine-checked pieces; upper bound P by transfer of
  Theorems 11.52, 11.54, 11.64, not refereed, nothing simulated.

## 3. Verification method and evidence inspected

1. **Read** (in this order): §11.26; THY-MSG-0011; THY-REQ-0011; `W_REPORT.md` in full (1185 lines); the two-letter
   proofs that are transferred — theory report §11.16, §11.18 (Theorems 11.52–11.54), §11.19 (11.56–11.58), §11.20
   (11.59–11.65, Lemma 11.62, Theorem 11.63 and its proof in `F_REPORT.md` §3.4–3.6: Lemma T, Lemma SL, six steps,
   Theorems F7–F9), §11.21 (Theorem 11.66), §11.23 (11.76–11.80), Theorems 11.22, 11.27, 11.28; `DEAD_ENDS.md` D52; the
   Lean statements used (`RenyiCentre.lean` whole; `GamePair.lean`: `GameFunction`, `pair`, `exactRec_*`;
   `HintRecursion.lean`: `HintPair`, `StepLE`, `iterates_lt_hint_add`; `GroupSampling.lean`: `lowDens_shift`,
   `truncate_admissible`, `group_queries_ge`, `group_nonadaptive_queries_ge`; `GeneralisedDips.lean`:
   `genDip_expected_queries_ge_exp_weights`; definitions `Admissible`, `slack`).  The authors' code `wv_lib.py` was read
   only after my own implementation had reproduced the numbers.
2. **Re-derived** on paper: the identity and its uniqueness statement; the dictionary; the limits `t → 0, 1`; the
   crossing identity; Lemma W1.0; Theorem W1(a)(i),(iii); W2(a); Lemma T′; W2(b) Steps 1–6; W2(c); W3(a), (b) (upper
   bound, vertex reduction, "attained", the cases `τ ≤ 1`/`τ ≥ 1`, window step), (c), (d), (e); Proposition W4.0; of
   Theorem W4: the facts (F1)–(F3), the tail lemma in the orientation `s(y→x)`, the union bound (M2), validity and width
   of the bracket, termination, the exponent of the outer sample, the use of Theorem 11.66.
3. **Replicated** with own code (numpy/scipy/mpmath; §6): vertices; the identity by three routes; every number of
   THY-MSG-0011 §1(c) and of the worked-example table for the six chains; the dictionary on the cube and on four
   chains; the three "fails beyond two letters" statements; the exact crossings; the single-letter evaluation lemma by
   a primal convex programme; the finite-`n` statements of the transfer by brute force on a 36-point space with two
   site types and two asymmetric envelopes; the typical-subset lemma by exact enumeration on 72 points.
4. **Lean**: a verbatim copy of `RenyiCentre.lean` with four `#print axioms` lines was elaborated with
   `lake env lean` (Lean 4.31.0, the project's Mathlib; no `lake build`): no error, axioms
   `[propext, Classical.choice, Quot.sound]` (`out/lean_check.txt`).

---

## 4. Established findings

### 4.1 The identity, with exact conventions [P — my derivation; N — replicated]

Conventions.  For laws `P, Q` on a finite set and `0 < t < 1`: `D_t(P‖Q) := (t−1)^{-1} ln Σ_a P(a)^tQ(a)^{1−t}` (natural
logarithm), so `(1−t)D_t(P‖Q) = −ln ΣP^tQ^{1−t} = t·D_{1−t}(Q‖P)`.  For a channel `W(a|φ)` and an input law `M`:

    I^S_t(M;W) := min_Q (t−1)^{-1} ln Σ_φ M(φ) Σ_a W(a|φ)^t Q(a)^{1−t} = (t/(t−1)) ln Σ_a (Σ_φ M(φ)W(a|φ)^t)^{1/t}        (Sibson)
    I^A_t(M;W) := min_Q Σ_φ M(φ) D_t(W(·|φ)‖Q)                                                                      (Augustin)
    C_t(W)     := max_M I^S_t(M;W) = max_M I^A_t(M;W) = min_Q max_φ D_t(W(·|φ)‖Q)                                    (capacity = radius)
    E_0(ρ, M)  := −ln Σ_a (Σ_φ M(φ)W(a|φ)^{1/(1+ρ)})^{1+ρ} = ρ·I^S_{1/(1+ρ)}(M;W)                                      (Gallager)

For `t < 1`, `I^S_t(M) ≤ I^A_t(M)` (Jensen), with equality at a capacity-achieving `M`.  The *vertex channel* of a site is
`W(a|φ) = π_φ(a)`, `φ ∈ 𝒱_j`.

**Proposition R5.1 (= Theorem 11.99, first display).**  Let `(π, d)` be a site (the triangle inequality of `d` is not
needed here), `0 < t < 1`, `m_M(a) := (Σ_φ M(φ)π_φ(a)^t)^{1/t}`, `G_t(M) := −t ln Σ_a m_M(a) = (1−t)I^S_t(M;W)`.  Then
(i) `F(γ,t) ≤ max_M G_t(M)` for **every** `γ ∈ ℝ^𝒮` (in `L` or not);
(ii) equality holds iff `π_γ = Q* := m_{M*}/Σ m_{M*}` for a maximiser `M*`; `Q*` is unique, and `γ* := −ln(Q*/π) ∈ L`;
(iii) `max_M G_t(M) = min_Q max_φ (1−t)D_t(π_φ‖Q)`, with the unique minimiser `Q*`.  Hence `F*(t) = (1−t)C_t(W)`.
*Proof.*  (i) `val(K^γ) = min_M max_a Σ_φ M(φ)(π_φ(a)/π_γ(a))^t = min_M max_a (m_M(a)/π_γ(a))^t ≥ min_M (Σ_a m_M(a))^t`, because
`Σ_a π_γ(a)·(m_M(a)/π_γ(a)) = Σ_a m_M(a)` and a mean is at most the maximum.  (ii) If `π_γ = Q*`, the mixture `M*` gives
`max_a (m_{M*}/Q*)^t = (Σ m_{M*})^t`, so `val ≤ e^{−G_t(M*)}`.  Conversely equality forces `m_{M₁} ∝ π_γ` for the optimal
`M₁` of the game and `G_t(M₁) = max G_t`; `s ↦ Σ_a s_a^{1/t}` is strictly convex, so `s* = Σ_φ M*(φ)π_φ^t` and `Q*` are unique.
`γ*(a) = −t^{-1} ln Σ_φ M*(φ)e^{−tφ̃(a)} + const` and `Σ_φ Me^{−tφ̃(b)} ≤ e^{td(a,b)}Σ_φ Me^{−tφ̃(a)}`, so `γ*(a) − γ*(b) ≤ d(a,b)`.
(iii) For fixed `M` the maximiser of `Q ↦ Σ_a s_aQ(a)^{1−t}` is `Q ∝ s^{1/t}` (Lagrange), with value `(Σ_a s_a^{1/t})^t`; so
`G_t(M) = min_Q −ln Σ_φ M(φ)c_φ(Q)`, `c_φ(Q) := Σ_a π_φ(a)^tQ(a)^{1−t}`, which is linear in `M` and concave in `Q`: Sion's theorem
gives `max_M min_Q = min_Q max_φ −ln c_φ(Q)`.  ∎
This is the proof of the report (its two elementary steps are the ones in `RenyiCentre.lean`), which I found
complete; (i) for `γ ∉ L` and the remark on the triangle inequality are small additions.

*Which definition makes it true.*  The stated programme is Sibson's information; maximised over `M` it equals the Rényi
radius, which is also the maximum of Augustin's (and Arimoto's) information — [K] Csiszár 1995 for finite alphabets,
Nakiboğlu 2019 in general (read: search snippets of arXiv:1608.02424; proved directly above, so nothing depends on
it).  **At a fixed `M` the two informations differ**, and this matters in one place: the exponent of a *given*
generalised cone with label law `M` (Theorem 11.98(d)) is the Csiszár–Körner form
`min{D(V‖W|M) : I(M,V) ≤ θ} = sup_ρ ρ[I^A_{1/(1+ρ)}(M) − θ]`, which is `≥ sup_ρ[E_0(ρ,M) − ρθ]` with strict inequality in general
([P] Lagrangian duality and `min_ν[KL(ν‖Q) + sKL(ν‖P)] = D_{s/(1+s)}(P‖Q)`, as in W_REPORT Theorem W3(e); [N] `t03`(C): 48 random
`M`, no violation of `Gallager(M) ≤ CK(M) ≤ E_sp`, gaps up to `3.5·10⁻³`, equality of all three at `M*` to `10⁻¹⁵`).  The theorem
is stated with the *maximised* `E_0`, for which Sibson and Augustin agree — correct; see m4.

*Limits* [P, re-derived; N].  `F*_j(t)/(1−t) = C_t ↑ C_1` (Shannon capacity) as `t ↑ 1`; `F*_j(t)/t = min_Q max_φ D_{1−t}(Q‖π_φ) ↑
min_Q max_φ KL(Q‖π_φ) = max_M −ln Σ_a Π_φ π_φ(a)^{M(φ)}` as `t ↓ 0` (both monotone, so the sharp constants of the game function
are the limits, and they add over site types).  Numerically the brackets `[max_M I(M;W), max_φ KL(π_φ‖Q_M)]` and
`[max_M −ln ΣΠπ_φ^{M}, max_φ KL(Q_M‖π_φ)]` close to `≤ 10⁻¹⁰`; `E_0(ρ)/ρ → a` and `E_0(ρ) → E` (path site: `0.294773` at `ρ = 10⁻⁴`
against `a = 0.294791`; `0.400510` at `ρ = 4000` against `E = 0.400622`).

### 4.2 The dictionary is algebra and needs no concavity [P — mine]

**Proposition R5.2.**  Let `F` be continuous on `[0,1]` with `F(0) = F(1) = 0`, and put `E_0(ρ) := (1+ρ)F(1/(1+ρ))` (`ρ ≥ 0`),
`R̂(e) := max_{0≤t≤1}[F(t) − te]`, `θ_na(x) := sup_{0≤τ<1}(F(τ) − τx)/(1−τ)`, `E_sp(θ) := sup_{ρ≥0}[E_0(ρ) − ρθ]`.  Then for
`θ ≥ 0`, `x ≥ 0` and real `e`:
(a) `R̂(e) = max{0, sup_{ρ≥0}(E_0(ρ) − e)/(1+ρ)}` and `θ_na(x) = max{0, sup_{ρ>0}(E_0(ρ) − x)/ρ}`;
(b) `θ_na(x) ≤ θ ⟺ E_sp(θ) ≤ x`;      (c) `R̂(e) ≤ θ ⟺ e ≥ E_sp(θ) − θ`;
(d) `θ_na(e + R̂(e)) = R̂(e)` whenever `R̂(e) > −e` (the pair identity).
*Proof.*  (a) substitute `t = 1/(1+ρ)`.  (b) `θ_na(x) ≤ θ` iff `E_0(ρ) − ρθ ≤ x` for all `ρ > 0` (and `0 ≤ x` covers `ρ = 0`).
(c) `R̂(e) ≤ θ` iff `E_0(ρ) − e ≤ θ(1+ρ)` for all `ρ ≥ 0`.  (d) with `θ = R̂(e)`, `x = e + θ`: `F(τ) − τx ≤ θ(1−τ)` for all `τ`, with
equality at a maximiser `t* < 1`.  ∎
So `x_na(θ) = E_sp(θ)` and `e_hint(θ) = E_sp(θ) − θ` (the shear law) for **every** continuous `F` — concave or not; this is
relevant because `F*` is not concave beyond two letters (§6.3).  With `F = F* = Σ_jλ_j(1−t)C_t(W_j)`:
`E_0(ρ) = ρΣ_jλ_jC_{1/(1+ρ)}(W_j) = Σ_jλ_j max_{M_j}E_0^{(j)}(ρ,M_j)` — Gallager's function **maximised over the input law of each
site type separately, at a common `ρ`** — and `E_sp` is the sphere-packing exponent of the memoryless channel that uses
`W_j` on the sites of type `j` ([K] additivity of `E_0` for parallel/time-varying use: Gallager 1968, from memory).  What is
*not* algebra: that `θ_na` is the non-adaptive exponent (Theorem 11.98(d)) and `R̂` the adaptive/hinted one (Theorem
11.101).  Numerically ([N] `t03`): on the cube (`u = 0.5, 1, 2`) `a = ln 2 − h(p_u)`, `E = ln cosh(u/2)`,
`F* = Λ(tu) − tΛ(u)`, `h = KL(Λ₁/u‖½)`, `E_sp(θ) = KL(ρ‖p_u)` at `KL(ρ‖½) = θ` (`p_u ≤ ρ ≤ ½`) and `E_sp(θ) − θ = uρ − Λ₁`, all to
`10⁻⁹`; on `path`, `asym`, `mix`, `mix2` the raw Gallager form `sup_ρ[E_0(ρ) − ρθ]` equals `S(R̂^{-1}(θ))` to `2·10⁻¹⁴` and
`E_sp(h) = h`.

**Range (finding m1).**  `E_sp(θ) − θ > 0` only for `0 < θ < h` (`h = R̂(0)` is the fixed point); for `h ≤ θ < a` a fixed sample
still certifies the extensive rate `E_sp(θ) > 0` while the adaptive rate is `0⁺`, and what an adaptive algorithm
achieves at sub-extensive accuracy is open beyond the uniform cube.  "Gains exactly `θ`" holds on `(0, h)` only.

### 4.3 The exact crossing [P — mine; N]

**Proposition R5.3 (= Proposition 11.103(e), the crossing).**  For `k ≥ 2`, `u > 0` let
`F_k(t) = tΨ_k(u) − Ψ_k(tu)`, `Ψ_k(s) = ln((e^s + k − 1)/k) − s/k`, and `h_k(u) = max_t F_k(t)`.  Then `F_k = (1−t)·I^S_t` of the
`k`-ary symmetric channel with correct-letter probability `e^u/(e^u + k − 1)` and uniform input, and with
`c_k := u^{-1} ln((e^u + k − 1)/k) ∈ (0,1)`:

    h_k(u) = ln k − H_b(c_k) − (1 − c_k) ln(k − 1)        (attained at e^{t*u} = (k−1)c_k/(1−c_k)).

At `e^u = k(k−1)`: `c_k + c_{k+1} = 1` and `h_k = h_{k+1}`.
*Proof.*  `F_k′(t) = 0` reads `e^{tu}/(e^{tu} + k − 1) = c_k`; inserting gives the closed form.  At `e^u = k(k−1)`:
`c_kL = ln((k−1)(k+1)/k)` and `c_{k+1}L = ln(k²/(k+1))` with `L = ln(k(k−1))`, whose sum is `L`; then
`h_k − h_{k+1} = ln k − ln(k−1) − ln(k+1) + c_kL = 0`.  ∎
[N] `t04`(e): to 40 digits for `k = 2..8`; the sign of `h_k − h_{k+1}` is `+` just below and `−` just above; the maximiser of
`h_k` over `k` obeys `(k−1)(k−2) ≤ e^u ≤ k(k−1)` for `u = 0.5, 1, 2, 3, 4, 6`.  ("Exactly when `u < ln 2`" for `h₂ > h₃`: the
identity is proved, the uniqueness of the crossing is numerical.)

### 4.4 The chain of statements behind the two theorems, and what I did with each

| statement (theory report / W_REPORT) | their label | my check | my verdict |
|---|---|---|---|
| Lemma W1.0: quotient envelope = oriented transport cost | P | re-derived; brute force `t06`(1): `4·10⁻¹⁶` | correct |
| 11.95(a)(i): orbit-wise quantile levels are admissible; truncation changes `ψ` on orbit density `≤ q` | V (`lowDens_shift`, `truncate_admissible`) + P | Lean statements read (general group, asymmetric `d`); the passage from `lowDens_shift` to the exact quantiles re-derived; brute force `t06`(5) | correct |
| 11.95(a)(ii), (b): `(1−2δ)/q` for non-adaptive / all algorithms | V (`group_nonadaptive_queries_ge`, `group_queries_ge`) | statements read (not the Lean proofs) | as labelled |
| 11.95(a)(iii): stratified sample | P | re-derived (Markov, multiplicative Chernoff) | correct |
| 11.95(c): `Z_gΦ_g⁺ ≤ Z_HΦ_H⁺` | P | re-derived; brute force `t06`(6) | correct |
| 11.97(a) = W2(a): lower bound at invariant instances, every `n` | P on V | re-derived | correct |
| Lemma 11.96 = T′ | P | re-derived line by line (rounding, most probable class, chain rule); exact enumeration `t09`: 640 cases | correct (m6) |
| 11.97(b) = W2(b): `Φ⁺(D) ≥ e^{ne} ⟹ maxdens(D) ≥ e^{−n[R̄_λ(e−ω_n)+ω_n]}` | P by transfer of 11.78(b) | Steps 1–6 re-derived | correct (m5) |
| **W2(c)**: the same for `μ_H` with `R̂`, `ω_n` independent of the composition | P (W_REPORT only) | re-derived; uses W3(b) and uniform continuity of `I − v` | correct; **not stated in the theory report (M1)** |
| 11.98(a) = W3(a): collapse to additive instances (Sion twice) | P | re-derived | correct |
| 11.98(b) = W3(b): `sup_μ φ_{μ,γ}(τ) = Σ_jλ_jF_j(γ_j,τ)`, vertex labels, one common slope; window step | P | re-derived (Kantorovich duality in the orientation used, Gibbs principle, Donsker–Varadhan, vertex reduction, Jensen); **primal test `t05`**: equality to `4·10⁻¹⁴` at the generalised-dip profiles of four chains (two with two site types), `V − R̂ ≤ −5·10⁻⁴` on 191 random (profile, budget) pairs and 24 perturbed optimal profiles | correct |
| 11.98(c), (d) = W3(d), (e): game function; non-adaptive exponent `θ_na`, lower bound every `n` | P; 11.66 V | re-derived (monotonicity of `F*/t`, `F*/(1−t)`; truncated generalised cones; the upper bound through W2(c)) | correct |
| 11.99 = W3(c), Remark W3.1 | P; two steps V | §4.1–4.2; Lean compiled | correct |
| 11.101(a) = W4.0 | P on V | re-derived; orientation of `slack`/`Admissible` in Lean matches; brute force `t06`(7) | correct |
| 11.101(b) = W4 | P by transfer | §4.5, §4.6 | proved with gaps (M1, M2) |

### 4.5 Theorem 11.101(b): the transfer, step by step

Against Theorem 11.52 (one more level), F7 (the same relative to a reference), 11.54 (levels), 11.63 (isoperimetry), 11.64
(with a field; repairs M1, M2 of referee R9).  "Requires" = what the step silently needs.

| # | step in the new setting (W_REPORT §5; theory report 11.101) | true? | argument given complete? | requires | verdict |
|---|---|---|---|---|---|
| 1 | Outer block: `⌊φn_j⌋` sites of *every* type, inner block the rest; both chains of the same kind | yes | yes | compositions of both blocks tend to `λ`: holds for every fixed `φ` (also for types with `n_j/n → 0`); W4 assumes all `λ_j > 0`, the theory report's statement does not say so (m9) | ok |
| 2 | (F1) fibres `b ↦ ψ(a,b)` are in `𝒞(X_i)` | yes | yes | additivity of `d` over sites | ok |
| 3 | (F2) `−ln W ∈ 𝒞(X_o)`, `W(a) = E_{π_i}e^{−ψ(a,·)}` | yes | yes | `π = π_o ⊗ π_i`: the inner law must not depend on `a` (the step that fails with interactions); brute force `t06`(3) | ok |
| 4 | (F3) layer cake | yes | yes | nothing | ok |
| 5 | Tail lemma relative to a reference in the orientation `s_ref(y,x) = d_o(y,x) − ψ_ref(y) + ψ_ref(x)` (`y ∉ D`, `x ∈ D`) | yes | yes (one line) | `D = {Ŵ > s} ≠ X_o`.  Brute force `t06`(4): 0 violations at 11 485 levels; 8 602 with the transposed slack | ok |
| 6 | Reference `ψ_H` of the outer block; `μ_H` sampled without evaluations; `Ŵ = W/w_H`; `A = Z_H·E_{μ_H}Ŵ` | yes | yes | `ψ_H ∈ 𝒞`: built with the **transposed** quotient envelope, `V_n(P) = min_{P′}[J_{P′} + δ(P′,P)]` (`t06`: the other orientation is not in the class) | ok |
| 7 | `s₀ ≤ min Ŵ`, `max Ŵ ≤ s₀e^{3nD_max}`; `J = ⌈3nD_max + b + c₁n + 10⌉` | yes | yes | oscillation of members and of `ψ_H` at most `nD_max`, `n_oD_max` | ok |
| 8 | (M2) potential inner calls `≤ 4K/min μ_H ≤ 4Ke^{c₁n_o}`, `c₁ = ln(1/π_min) + 1`; inner failure probability `δe^{−c₁n}/(2⁶n⁴)` | yes | yes | `μ_H(a) ≥ π_o(a)/N_orb` (`v ≥ 0`, `Z_H ≤ N_orb`); the exponent-function definition allows failure probabilities `e^{−cd}` | ok |
| 9 | Closure with `Ξ̄ ≥ Ξ_H`, zero below `min μ_H`, never at `q = 1` | yes | yes | `Ξ_H` itself is admissible (a finite maximum; no evaluations) | ok |
| 10 | Good event, validity, width, termination, `M ≤ 8Je²M†`, the count of points close to a level, the cost sum: "measure-free, verbatim" | validity, width, termination, `M ≤ 4K/min μ`: yes (re-derived for a general outer measure) | the count and the cost sum: taken from Theorem 11.52 (read; not re-derived) | i.i.d. outer sample from `μ_H`; Chernoff at `O(n³)` fixed thresholds | ok, inherited |
| 11 | Exponent of the outer sample: `M† ≤ exp(nφθ_na((g−β)/φ) + o(n))`, "uniformly over the compositions of the outer block" | yes | **compressed** (a parenthesis: "`ω_n` does not depend on the composition and `R̂` is continuous in `λ`"; what is needed is a statement about `θ_na`) | W2(c) with `ω_n` independent of the composition; closed in §4.6 | gap (M2), closed |
| 12 | The isoperimetric input: W2(c), by Lemma T′ + evaluation lemma (Kantorovich duality, separation over site types, vertex reduction) + window step by an optimal coupling + Hoeffding for the transport cost and all letter counts + chain rule conditional on the site type + `μ_H ≥ Q^⊗e^{−nω′}/N_orb` on a typical set | yes | yes in W_REPORT §3.3, §4 (constants loose: m5, m6) | product `π`; `I − v` uniformly continuous and zero on the window; `(M+1)^{q_max} ln n = o(n)` (hence the rate `n^{−1/(2q_max+2)}`) | ok; **only in the workstream report (M1)** |
| 13 | The pair: `F*` is a game function, not necessarily concave | yes | yes | Lean `GameFunction` has no concavity hypothesis (checked) | ok |
| 14 | Levels: base family = complete enumeration, `T₁ ≡ Σ_jλ_j ln q_j`; induction of Theorem 11.54 "with dimension read as chain with composition tending to `λ`" | yes | **compressed**: families indexed by compositions and their exponent functions are not defined | definition and uniformity of §4.6; Lean: `iterates_lt_hint_add` with `hbdd` (any bounded start) and `GameFunction.pair`, not `exactRec_tendsto` (m7) | gap (M2), closed |
| 15 | Lower bound: W4.0 at `γ*(ε₁)` | yes | yes | — | ok |

Answers to the questions of the brief.  *Finitely many site types with positive fractions:* finitely many, yes
(`m`, `q_max`, `D_max`, `π_min` enter all error terms); positivity is assumed in W4 and is not needed by the argument as
far as I can see, but the theory report's statement should say which.  *Envelope asymmetry:* handled; the two places
where the orientation can go wrong (the slack of the tail lemma; the envelope in `V_n`) are right, and wrong
orientations are detected by brute force.  *Non-concave site functions:* harmless — the Lean pair theorem, the
dictionary (Proposition R5.2) and both exponent formulas hold without concavity; only "the best split of the accuracy is
exact" needs it, and the report says so.  *Tail lemma relative to a reference for more than two letters:* one line,
correct.  *The isoperimetric input:* it is W2(c) — **proved (paper) in the workstream report, not cited from the
literature and not merely asserted**; it uses no covering or type-covering lemma (the sampler is `μ_H` itself) and no
finite-`n` extremal statement; its only external ingredients are Hoeffding's inequality, Sion's theorem, Kantorovich
duality for a quasi-metric cost and the integrality of transportation polytopes ([K], standard; from memory).

### 4.6 The two gaps of the written proof, closed [P — mine]

**(G1) Families indexed by compositions.**  Fix the site types and `λ`.  A chain is a vector `𝐧 = (n_1..n_m)`,
`|𝐧| = Σn_j`.  A *family* gives, for every `(𝐧, x > 0, δ′)`, a bracket procedure of accuracy `x` and failure probability `δ′`
on the chain `𝐧`, of cost `C(𝐧, x, δ′)` nonincreasing in `x` and `δ′`.  `T` is an *exponent function of the family at `λ`* if
for all `ξ, c > 0`

    lim_{η↓0} limsup_{N→∞} sup{ |𝐧|^{-1} ln C(𝐧, ξ|𝐧|, e^{−c|𝐧|}) : |𝐧| ≥ N, ‖𝐧/|𝐧| − λ‖₁ ≤ η } ≤ T(ξ)

(equivalently: along every sequence of chains with compositions tending to `λ`).  With this definition the induction
of Theorem 11.54 goes through verbatim: the inner block of a chain within `η` of `λ` is within `η + m/((1−φ)|𝐧|)` of `λ` **[note added at checkpoint 38: `2m/((1−φ)|𝐧|)` — `m` is wrong for three or more site types; found by the theory division (THY-RES-0007 §1.4(a)), re-derived by workstream R9; immaterial for the theorem]**,
only finitely many rates occur, and the one-level bound is uniform by (G2).

**(G2) Uniformity of the outer exponent.**  Let `λ°` be the composition of the outer block (`n_o` sites), `x > 0`,
`ω′ := ω_{n_o} + ln 4/n_o` with `ω_n` of W2(c), and `n_o` so large that `x > 2ω′`.  *Claim:* if `θ > θ_na^{λ°}(x − 2ω′) + ω′`, then
`Ξ_H(e^{−n_oθ}) ≤ e^{−n_oθ}e^{n_ox}/4`.
*Proof.*  Otherwise some `D` has `μ_H(D) ≤ e^{−n_oθ}` and `Φ_H⁺(D) ≥ e^{n_o(x−θ)}/4`; W2(c) gives `θ ≤ R̂(e′) + ω′` with
`e′ := x − θ − ω′`, hence `S(e′) = e′ + R̂(e′) ≥ x − 2ω′`, hence `θ_na(x − 2ω′) = R̂(S^{-1}(x − 2ω′)) ≥ R̂(e′) ≥ θ − ω′` (all functions for the
composition `λ°`; `R̂` nonincreasing, `S` increasing).  ∎  So `q† ≥ exp(−n_o[θ_na^{λ°}(x − 2ω′) + ω′])` — for all `θ` at once; no
restriction to compact sets of `θ` is needed.  Finally `θ_na` depends on the composition in a uniformly Lipschitz way:
`F*_{λ′}(τ) − F*_λ(τ) = Σ_j(λ′_j − λ_j)F*_j(τ)` and `F*_j(τ) ≤ a_j(1−τ)` give

    | θ_na^{λ′}(x) − θ_na^{λ}(x) | ≤ ‖λ′ − λ‖₁ · max_j a_j        for all x > 0,

and `θ_na^λ` is continuous on `(0,∞)` ([V] `GameFunction.pair`, field `na_cont`).  Hence
`M† = 2K/q† ≤ exp(nφθ_na^λ((g−β)/φ) + o(n))` uniformly over chains with compositions near `λ`.  The same bound serves
Theorem 11.98(d) (the non-adaptive upper bound) along sequences of compositions.

### 4.7 The Lean file `RenyiCentre.lean`

Four theorems, all about real vectors on a finite type; no `sorry`; axioms `[propext, Classical.choice, Quot.sound]`
([V], compiled by me from a verbatim copy):

* `scale_le_inv_sum`: `ΣP = 1`, `Σm > 0`, `c·m ≤ P` pointwise `⟹ c ≤ 1/Σm`.
* `exists_ratio_le`: `ΣP = 1`, `m > 0` pointwise `⟹ ∃a, P a/m a ≤ 1/Σm` — the inequality `min_a(P/m) ≤ 1/Σm` behind (i).
* `eq_of_forall_ratio_ge`: if every ratio is `≥ 1/Σm` then `P = m/Σm` — the equality case behind (ii).
* `softmin_admissible`: if every `φ_i` satisfies `φ_i a − φ_i b ≤ d a b`, then so does
  `a ↦ −t^{-1} log Σ_i M_i exp(−tφ_i a)` for `t > 0`, `M ≥ 0`, `ΣM > 0`; `d` arbitrary (no symmetry, no triangle inequality).

They are exactly "the two elementary steps" named in the theorem header (the first step is three declarations).
Hypotheses are satisfiable (any probability vector `P`, any positive `m`); the statements are not vacuous.  **Not
covered:** the definition of a site, its polytope, vertices or Gibbs laws; the minimax theorem and the rewriting of
the game value as `min_a(π_γ/m_M)^t`; uniqueness of the centre; Sibson's identity and the radius form; the limits; the
dictionary; anything operational.  The header of the Lean file says so itself.  So Theorem 11.99 is a **paper proof
with two machine-checked lemmas**, as labelled.  The other machine-checked inputs of §11.26 (`GroupSampling.lean`,
`GeneralisedDips.lean`, `GamePair.lean`, `HintRecursion.lean`) were read at the level of statements only: they are stated
for an arbitrary finite space, an arbitrary (possibly asymmetric) envelope and an arbitrary finite symmetry group, and
`GameFunction` has no concavity hypothesis.

### 4.8 Headline against theorem

"Certification cost is a channel-coding exponent" (THY-MSG-0011 title; README (xi)).  What is proved, for which
algorithms, accuracies, instances and `n`:

| half | algorithms | accuracy | instances | `n` | status |
|---|---|---|---|---|---|
| `≥ (1−2δ)exp(−tε + nΣλ_jF_j(γ_j,t))` evaluations | all (randomised, adaptive, with any hint) | every `ε > 0` | cost at the additive instance `γ` (so: worst case `≥ e^{nR̂(ε₁)}` at `γ*`) | every `n` | P on V inequalities (product step on paper; re-derived, brute-forced) |
| `≥ (1−2δ)/q` if `ε < ε_n^{tr}(q)` | non-adaptive | every `ε` | a pair `(ψ, ψ^{tr,q})` of class members | every `n` | V; the *value* `ε_n^{tr}(e^{−nθ}) ≥ nE_sp(θ) − O(log n)` by truncated generalised cones: P |
| joint-type-stratified sample is correct at `ε ≥ ε_n^{tr}(q) + ln(4/δ)` with `N_orb⌈8 ln(2N_orb/δ)/q⌉` points | — | every `ε` | whole class | every `n` | P.  So the non-adaptive complexity is `1/q` up to a polynomial factor for every `n`; that `ε_n^{tr}(e^{−nθ}) ≤ nE_sp(θ) + o(n)` needs W2(c): `n → ∞` only |
| adaptive, no hint: `exp(nR̂(ε₁) + o(n))` suffice | the nested algorithm; the number of levels grows as the exponent is approached | extensive, `0 < ε₁ < E` | whole class (worst case) | `n → ∞`, compositions `→ λ`; `o(n)` unquantified (the proof gives `ω_n ~ n^{−1/(2q_max+2)}` per level) | P by transfer (§4.5); never simulated |
| with a hint: `exp(nR_λ(ε₁) + o(n))` suffice | hedged spot-check | extensive | instances that are functions of the joint type (incl. additive ones) | `n → ∞` | P (W2(b)); at other instances only through the previous row |
| bounded accuracy, `ε = O(1)` | — | — | — | — | only the lower bounds (`h` for all, `a` for non-adaptive algorithms); upper bounds exist for the uniform cube only (§11.19) |
| above the threshold: bounded cost | sampling one product law | `ε₁ > E` | whole class | every `n` | V for identical sites (Theorem 11.28(d)); several types on paper |

So the dictionary is a statement about **worst-case exponents at extensive accuracy for a class with a known product
measure**: the lower halves hold for every `n`; the upper halves are asymptotic paper proofs, the adaptive one an
existence statement.  The theorem texts say this (11.101: "exponents at extensive accuracies, with unboundedly many
nested levels; not an algorithm to run"); the README sentence "A fixed sample of `e^{nθ}` evaluations certifies the
accuracy rate given by the sphere-packing exponent …; adaptivity, or a hint, gains exactly `θ`" omits the range
`θ < h`, the word "asymptotically", and that with a hint it is a statement about the hardest instance (m1).

---

## 5. Findings

### Critical

None.

### Major

**M1.  The isoperimetric input of Theorems 11.98(d) and 11.101(b) is not stated in the theory report.**
*Location:* `THEORY_REPORT.md` l. 6200–6216 (Theorem 11.97 has parts (a), (b) only), l. 6235–6238, l. 6302–6309 ("whose
exponent is Theorem 11.97 in the form for `μ_H`"); the statement is `W_REPORT.md` l. 296–302 (Theorem W2(c)), its proof
l. 367–376 together with l. 407–411 and 478–482.  *What is wrong:* both upper bounds rest on

    Φ_H⁺(D) ≥ e^{ne}  ⟹  μ_H(D) ≥ exp(−n[R̂(e − ω_n) + ω_n])    for all n, e, D ⊊ X,   ω_n → 0 depending on the site types only, not on the composition,

which differs from Theorem 11.97(b) in two ways that matter (the measure `μ_H` instead of the largest orbit density,
which needs the window step and the continuity of `I − v`; the evaluated function `R̂` instead of the supremum `R̄_λ`), and
whose uniformity in the composition — mentioned for (b) in one clause — is what the nested algorithm depends on,
because blocks have compositions that are only asymptotically `λ`.  *Why it matters:* it is the single
non-elementary input of the transfer and the place where a reader has to trust the workstream report; the theory
report's status line ("proofs by transfer … with every changed step written out in the report") is true only of
`W_REPORT.md`.  *Substance:* I re-derived the proof (Steps 1–6, Lemma T′, the evaluation lemma, the window step) and
found it correct; the constants are loose (m5, m6).  *Correction:* add it as Theorem 11.97(c) with the uniformity
clause and a pointer to the six steps; have it refereed together with Theorem 11.78(b).

**M2.  Theorem 11.101(b): the level induction is transferred with an undefined notion and an unproved uniformity.**
*Location:* `W_REPORT.md` l. 662–671 and 677–682; `THEORY_REPORT.md` l. 6308–6309 ("families of procedures are indexed by
compositions").  *What is wrong:* "exponent function … defined along sequences of compositions tending to `λ`" is not
defined; the bound on `M†` is claimed "uniformly over the compositions of the outer block" on the grounds that `R̂` is
continuous in `λ`, while the quantity used is `sup{θ : θ + R̂^{-1}(θ) ≥ x}`, for which continuity in `λ` of an inverse
function would have to be argued; and it is restricted to compact sets of `θ` without need.  *Why it matters:* the
induction applies the one-level theorem to inner blocks whose compositions differ from `λ` at every level; without a
uniform statement the "verbatim" transfer of Theorem 11.54 is not a proof.  This is the same kind of gap as (M1) of
referee R9 for the two-letter proof.  *Correction:* §4.6 — the definition (G1), the direct argument (G2) and the bound
`|θ_na^{λ′} − θ_na^λ| ≤ ‖λ′ − λ‖₁ max_ja_j`.  With these the gap is closed; no exponent changes.

### Minor

**m1.  The dictionary sentence lacks its range and its mode** (`THEORY_REPORT.md` l. 6255–6257; README l. 356–358;
THY-MSG-0011 l. 49–50).  "A fixed sample certifies `E_sp(θ)`" is for `0 < θ < a`; "an adaptive algorithm, or one with a
hint, certifies `E_sp(θ) − θ`" only for `0 < θ < h` (beyond, the expression is `≤ 0`: e.g. `−0.008` at `θ = 0.3a` on the cube with
`u = 1`), is asymptotic at extensive accuracy, and with a hint refers to the hardest instance.  Also `R̂(e) = max_ρ…` should
be `sup` (for `e ≥ E` the supremum `0` is a limit).  *Correction:* "for `0 < θ < h` … at the exponential scale, in the worst
case over the class".

**m2.  A garbled sentence in "Why the sphere-packing exponent appears"** (l. 6270–6272): "truncating the cone removes
the rest, whose Gibbs mass is `exp(−n·min{D(V‖W|M) : I(M,V) ≤ θ})`".  That exponent is the Gibbs mass of the outputs the
sample *sees* (what remains after truncation); the rest carries almost all the mass.  *Correction:* "… removes the
rest; what remains has Gibbs mass `exp(−n·min{…})`".

**m3.  Machine-checking is described more strongly in the status lines than in the theorem headers** (l. 6160–6162:
"Machine-checked: the every-`n` lower bounds"; README l. 362–363).  Machine-checked are the general inequalities
(`group_queries_ge`, `group_nonadaptive_queries_ge`, `genDip_expected_queries_ge_exp_weights`, the truncation); the product
step for several site types (independent labels, Markov's inequality, the identification with `nΣλ_jF_j`), the
evaluation of `ε_n^{tr}` for truncated cones and the multi-type form of Theorem 11.28 are paper steps (the Lean files
treat identical sites).  The headers of Theorems 11.95 and 11.101 say this correctly ("P from machine-checked
pieces"); the status paragraph and the README should use the same words.  (The same defect was "major" in the review
of §11.16, D43; here it is confined to two summary sentences.)

**m4.  "Gallager's function `E_0(ρ) = ρ·Σ_jλ_jC_{1/(1+ρ)}`"** (l. 6250–6251) is Gallager's function *maximised over the input
law of each site type separately*; Gallager's `E_0(ρ, M)` for a given `M` is `ρI^S_{1/(1+ρ)}(M)`, and the exponent of a given
generalised cone is the Csiszár–Körner/Augustin form, which is strictly larger for non-optimal `M` (§4.1).  The theorem
is right; one clause would prevent a reader from inserting `E_0(ρ, M)` into the cone formula.

**m5.  Hoeffding step of the isoperimetric proof** (`W_REPORT.md` l. 351–356): "all of them are within `nδ₁·max(D_max,1)` of
their means" does not give the next inequality when `D_max > 1` (the transport term would carry `D_max²`); with the cost
within `nδ₁D_max` and each letter count within `nδ₁` — which is what Hoeffding gives with the stated probability — the
bound `B − δ` follows.  Constants only.

**m6.  Lemma T′ is stated for site laws of full support and applied with `ρ = ⊗P_{τ(i)}`**, `P` the joint type of the
piece (`W_REPORT.md` l. 307, 343), which may miss letters.  Restrict the alphabets to the support (the proof only
evaluates `ln(u(a)/ρ_j(a))` at letters that occur).

**m7.  The Lean theorem behind step (ii)–(iii)** (`W_REPORT.md` l. 673–677; theory report l. 6232–6234, 6292–6310).  With
the base family "complete enumeration" the level recursion does not start at `θ_na`, so
`GameFunction.exactRec_tendsto` (Theorem 11.66(c)) is not the statement that applies; the one that does is
`iterates_lt_hint_add` (hypothesis `hbdd`: any bounded start) with the `HintPair` from `GameFunction.pair`, as in the
proof of Theorem 11.64.  That the iterates `T_{k+1} = min(T_k, R[T_k])` satisfy `StepLE` is immediate and on paper.

**m8.  A published number.**  `W_REPORT.md` l. 563: "slope jump `+0.0052`" at the label switch of the triangle site; I get
`+0.00558` (branch slopes `0.054049` and `0.059631` at `t_c = 0.377987`; `t04b`).  `t_c`, the corner `0.1996·E`, the slopes
`−0.383 → −0.373` of `R̂` and the defect `8·10⁻⁷` of the best split on `mix2` are reproduced.

**m9.  Hypotheses of Theorem 11.101(b)** (l. 6298–6301).  State `0 < δ < ½` fixed, "chains with compositions tending to
`λ`" with or without `λ_j > 0` (W4 assumes it; the argument does not seem to need it), and that the `o(n)` depends on the
site types and on `(ε₁, δ)` but not on the sequence of compositions (this is what §4.6 gives).

**m10.  Status of Theorem 11.78(b)** (l. 6150–6151: "refereed 'proved' by R10 as this checkpoint was closed; its report
is applied at the next one").  At `89ac710` the tree contains `docs/reviews/R10_brief.md` but no R10 report, so the
statement cannot be checked from the repository.  It is not load-bearing for §11.26 (the six steps are written out in
`W_REPORT.md` and I checked them there), but the sentence should cite a file.

**m11.  "The labels that carry weight are exactly at Rényi distance `C_t`"** (`W_REPORT.md` l. 424).  One direction only:
labels in the support of `M*` are at distance `C_t` from the centre (complementary slackness); a vertex at that distance
need not carry weight, and `M*` need not be unique (`s*` is).

**m12.  Numerical hygiene (theirs and mine).**  `wv_lib.py` solves the game with the default tolerances of HiGHS
(`10⁻⁷`); a blind maximisation over `γ` of such values is biased upwards by the solver noise.  My first run showed the
"definition" route *exceeding* the Rényi value by `2–3.5·10⁻⁹` on `path` and `asym`; with tolerances `10⁻¹⁰` and the value
re-evaluated from the returned strategy the excess is `≤ 6·10⁻¹⁶`.  Not an error of the report (its checks are at
`5·10⁻⁷`), but a test "blind search never exceeds the closed form" needs this care.  A second trap of my own: counting
`w = t_P` as "changed by the truncation" after `−ln(exp(−ψ))` produced 330 spurious violations of Theorem 11.95(a) until
a tolerance was used.

---

## 6. Reproduction status (independent replication; my values next to theirs)

All with `experiments/science/ws_R5/r5lib.py`: brute-force vertex enumeration; the game by linear programming; the
Rényi programme in `M` (SLSQP with the analytic gradient `∂G/∂M(φ) = −exp(G − (1−t)D_t(π_φ‖Q_M))`); the dual programme in `Q`
(a different programme, no `M`); every value bracketed by `[G_t(M), max_φ(1−t)D_t(π_φ‖Q)]`.

### 6.1 The identity (`t01_identity.py`)

56 site/slope pairs (the four example sites at `t = 0.1…0.9`; 36 random sites with asymmetric envelopes, `q = 2, 3, 4`):
blind maximisation over `γ ∈ L` of the linear-programming value = primal = dual = linear-programming value at the
Rényi centre, largest deviation `9·10⁻¹³`; the centre is in `L` in every case; the blind search never exceeds the Rényi
value (largest excess `6·10⁻¹⁶`); `F(γ,t) ≤ F*(t)` also for 1600 random `γ` outside `L`; Gallager's raw `E_0(ρ,M)` equals
`G_t(M)/t` to `5·10⁻¹⁶`.  Vertices: `bin` 2, `path` 4, `tri` 6, `asym` 5, as in the report.

### 6.2 Reference numbers (`t02_reference_numbers.py`, `t07_misc.py`, `t07b_zero_threshold.py`)

| chain | quantity | theirs | mine | diff |
|---|---|---|---|---|
| `path` (THY-MSG-0011 §1(c)) | `E` | `0.400622` | `0.400622034` | `3·10⁻⁸` |
| | `a` | `0.294791` | `0.294791205` | `2·10⁻⁷` |
| | `R(0) = h` | `0.089589` | `0.089589021` | `2·10⁻⁸` |
| | `R(0.3E)` | `0.043375` | `0.043375` | `2·10⁻⁷` |
| | `θ_na(0.3E)` | `0.066899` | `0.066899057` (also as `R̂∘S^{-1}`: same to `10⁻¹⁵`) | `6·10⁻⁸` |
| | zero residual `R_0(0)` | `0.080032` | `0.080032` | `4·10⁻⁷` |
| | best coarse-graining / deletion | `0.048586` / `0.115369` | `0.048586` / `0.115369` | `3·10⁻⁷` |
| | centre law; `γ*`; labels | `(0.473, 0.246, 0.281)`; `(0, 0.1454, −0.3946)`; dips at the two ends `0.504/0.496` | `(0.4734, 0.2456, 0.2810)`; `(0, 0.1454, −0.3946)`; `0.5039/0.4961` on `(0,−0.8,−2.4)`, `(0,0.8,2.4)` | — |
| | threshold of the zero residual | `0.394664` | `0.394664` (as a limit: one LP) | `1·10⁻⁷` |
| `bin` | `E, a, h, R(0.3E), θ_na(0.3E)` | `0.103131, 0.095301, 0.025034, 0.012209, 0.019941` | same | `≤ 5·10⁻⁷` |
| `tri` | `E, a, h, R(0.3E), θ_na(0.3E), R_0(0)` | `0.284907, 0.247541, 0.066729, 0.032077, 0.051124, 0.065233` | same | `≤ 3·10⁻⁷` |
| `asym` | the same six | `0.191059, 0.166046, 0.045407, 0.022108, 0.035544, 0.033856` | same | `≤ 5·10⁻⁷` |
| | `R_0/R̂` at `e = 0`, `0.7E`; zero-residual threshold | `0.75`, `0.15`; `0.155521` | `0.746`, `0.146`; `0.155521` | — |
| `mix` | the same six | `0.251877, 0.195046, 0.057275, 0.027759, 0.043288, 0.052360` | same | `≤ 4·10⁻⁷` |
| | average at a common accuracy against `R̂`, `e/E = 0.3, 0.5, 0.7, 0.9` | `+8.5 %, +47 %, +172 %, +1365 %` | `+8.5 %, +47.3 %, +172.0 %, +1365.0 %` | — |
| `mix2` | the same six | `0.212197, 0.186645, 0.050050, 0.024122, 0.038641, 0.049065` | same | `≤ 5·10⁻⁷` |

Largest deviation over the table: `5.0·10⁻⁷` — the rounding of the published six decimals.  Two-letter asymmetric
envelope = symmetric envelope with a tilted law (Proposition 11.102): `3·10⁻¹⁶` on six random sites, one of them
one-sided.

### 6.3 "Fails beyond two letters" (`t04_beyond_two_letters.py`, `t04b_kink.py`, `t04c_split.py`, `t07_misc.py`, `t07c_rare_third_state.py`, `t08_binary_concavity.py`)

| statement | theirs | mine |
|---|---|---|
| triangle site: `F*` not concave; label switch | `t_c = 0.378`; {dip 2, anti-dip 2, dip 0} `(0.506, 0.431, 0.063)` → three dips `(0.466, 0.389, 0.145)`; slope jump `+0.0052`; corner of `R̂` at `0.1996E`, slopes `−0.383 → −0.373` | `t_c = 0.377987`; `(0.506, 0.431, 0.064)` → `(0.466, 0.390, 0.144)`; slope jump **`+0.00558`**; `0.1996E`, `−0.383 → −0.373`; second difference `+4.9·10⁻⁶` at `t = 0.378` on a grid of step `10⁻³` (all others `< 0`); concave envelope `− F*` up to `6.8·10⁻⁶` |
| `mix2`: best split is not exact | by `8·10⁻⁷` (relative `2.5·10⁻⁵`) | `7.95·10⁻⁷` (`2.5·10⁻⁵`) at `e = 0.043306` |
| three letters, Hamming, `u = 1`: thresholds | `0.119499` (uniform) `< 0.120115` (two-letter cube) `< 0.120196` (`π = (0.05, 0.5, 0.45)`) | `0.119499092`, `0.120114507`, `0.120196008` (brackets closed to `10⁻¹¹`) |
| `h₂ > h₃` iff `u < ln 2`; values at `u = 0.5` | `0.007673` against `0.007425` | `0.007673`, `0.007425`; crossing at `u = 0.693147181`; a site law `((1−η)/2, (1−η)/2, η)`, `η ≤ 10⁻²`, has the two-letter value; the sign of the difference to the uniform law flips between `ln 2 ∓ 0.02` |
| `a₂ > a₃` iff `u < 0.5194`; values at `u = 0.3` | `0.011125` against `0.010582` | `0.011125`, `0.010582`; crossing at `0.519366` |
| uniform four letters, `u = 1` | `h = h₂ = 0.029139`, `a = a₄ = 0.117993`, `E = E₂ = 0.120115` | same; `F* = max(F₂, F₄)` to `4·10⁻¹⁵`, switch at `t = 0.6458` (theirs `0.65`) |
| uniform `q = 3, 4`, `u ∈ {0.5, 1, 2, 3}`: `E, a, h` = best equal grouping | stated | confirmed to `10⁻¹³` in all 24 cases |
| crossing `e^u = k(k−1)` | exact (P) | Proposition R5.3; 40 digits for `k = 2..8` |
| uniform law is hardest for `h`, `a` on 171 laws at `u = 1` | workstream (grid of 171 laws) | confirmed on the 171 laws with entries in `(1/20)ℕ`: grid maxima `h = 0.030572`, `a = 0.122951` (at permutations of `(0.35, 0.35, 0.3)`) below the uniform law's `0.030654`, `0.123284`; grid maximum of `E` is `0.120196` at `(0.05, 0.5, 0.45)` |
| two letters: `F*` concave in 100 cases | numerical, no proof | 16 sites of their kind and **500 random two-letter sites with vertex-law logits up to `±14`** (`t08`): no positive second difference on `t = 0.02 … 0.98`, step `0.01` (largest second difference `−3.5·10⁻⁶` of `max F*`); still no proof |

**An addition to Proposition 11.103(d) (which site law is hardest) [N, certified brackets; one line P].**  At the small
slope `u = 0.5` the same grid of 171 laws has its maximum of **all three** of `h`, `a`, `E` at `π = (0.05, 0.5, 0.45)`, and the
values exceed not only the uniform three-letter site but also the two-letter cube (`t07`, `t07c`):

| `u = 0.5`, Hamming, three letters | `h` | `a` | `E` |
|---|---|---|---|
| uniform law | `0.007425205` | `0.030166900` | `0.029097814` |
| two-letter cube | `0.007672866` | `0.030299862` | `0.030929804` |
| `π = (0.05, 0.5, 0.45)` | `0.007675166` | `0.030321669` | `0.030931644` |
| `π = (0.001, 0.4995, 0.4995)` | `0.007672975` | `0.030300641` | `0.030929982` |

So "site laws close to `(½, ½, 0)` have the two-letter values" is the limit; a *rare* third state is strictly harder than
the two-letter cube for `h` and `a` as well, not only near the threshold at `u = 1` (the report's `0.120196` against
`0.120115`).  One half of this is a theorem: **for the Hamming envelope, every site law that gives some set `A` of letters
the weight `½` satisfies `F*(t) ≥ F*_cube(t)` for all `t`** (the two box vertices `∓u·1_A` have Gibbs laws that differ only
through the indicator of `A`, where they form the binary symmetric channel with crossover `1/(1+e^u)`; this is the
coarse-graining bound of W_REPORT §6.2 at a balanced cut) — hence `h, a, E, R̂, θ_na` are at least the cube's; the strict
excess is numerical.  Which site law is hardest remains open; at `u = 0.5` the supremum is not approached as a letter
becomes rare (the two-letter values are the limit there), and at `u = 1` it is the uniform law for `h` and `a` but not for `E`.

### 6.4 The steps behind the transfer

* `t05_evaluation_lemma.py` — the single-letter lemma `V(μ, B; v) ≤ R̂(B − α(μ))` by a primal convex programme over exit
  profiles, optimal couplings and the minorant `v` (no game, no vertex labels in the bound, no slope): equality to
  `≤ 4·10⁻¹⁴` at the generalised-dip profiles of `asym`, `tri`, `mix` (binary + path) and of a chain with two three-letter
  types (`asym`/`tri`, fractions `0.3/0.7`) at `e = 0, 0.3E, 0.6E`; 191 random (profile, budget) pairs, negative accuracies
  included, and 24 perturbations of the optimum: `V − R̂ ≤ −5·10⁻⁴`.  This is an independent confirmation of "one common
  slope" for two site types.
* `t09_lemma_Tprime.py` — Lemma 11.96 by exact enumeration: five sites of two types in the order `(A, B, A, B, B)` (72
  points), 160 sets of four kinds, `M ∈ {1, 2, 3, 5}`: no violation of (2), (3), of the chain-rule identity
  `I(X_I; V | U_I, T_I) = α_Ã − α` (to `10⁻¹⁰`) or of its bound in 640 cases.
* `t06_bruteforce_orientation.py` — 36 points, two site types, both envelopes asymmetric, 400 random members of the
  class: quotient envelope = transport cost (`4·10⁻¹⁶`); dip formula and minimality; fibre averages admissible; tail
  lemma relative to `H`: 0 violations at 11 485 levels, 8 602 with the transposed slack; quantile truncation; `Z_gΦ_g⁺ ≤
  Z_HΦ_H⁺`; generalised dips with independent vertex labels are admissible, raise `ln A` by at least `r`, and a point lies in
  the support with probability at most `0.91·e^{tr}Π_jρ_t(M_j)^{n_j}` (40 random `(γ, t, r)`).
* Theorem 11.101(a) at `n = 480` on `mix`, accuracy `0.3En + 1 = 37.27`: `(1−2δ)·4.5·10⁵` evaluations at `γ*` (`max_t[nF*(t) − tε] =
  13.01`).  The report's `(1−2δ)·1.9·10⁶` at the same size comes from exact sums over joint types, which I did **not**
  re-run; the two are consistent (the exact sum must be the larger).

**Not replicated:** the exact sums over joint types (`n ≤ 480`) and their extrapolations; the brute-force runs on `3⁸`,
`2⁴3⁴`, `3⁷` points; the isoperimetric families (`w10`); the mean-field Potts numbers of Proposition 11.103(b); the level
recursion numerics.  Not run by anyone: the nested algorithm.

---

## 7. Originality assessment (one paragraph; the deep search is workstream A1's)

The identity is elementary once the game is written as `min_a(π_γ/m_M)^t` and the authors say so; every formula of the
dictionary is classical: Sibson's information and the information radius (Sibson 1969 — from memory, unverified);
capacity = radius for all three definitions on finite alphabets (Csiszár 1995) and in general, with a unique centre
(Nakiboğlu, *The Rényi capacity and center*, arXiv:1608.02424 — search snippets of the abstract and of Theorem 1);
`E_0(ρ,p) = ρI_{1/(1+ρ)}(p;W)` (same source, snippet); the sphere-packing exponent and its constant-composition form
(Shannon–Gallager–Berlekamp 1967; Gallager 1968; Csiszár–Körner — from memory; Nakiboğlu, arXiv:1611.06924 — snippet).
Three classical readings that the report does not mention seem worth adding, because they say what the dictionary
*is*.  (i) **Hypothesis testing** (Blahut, *Hypothesis testing and information theory*, IEEE Trans. IT 20 (1974)
405–417 — search snippet confirms the paper and its "sphere-packing-like bounds"; the content from memory):
`E_sp(θ) = sup_ρ ρ[C_{1/(1+ρ)} − θ]` is Hoeffding's trade-off `sup_ρ ρ[D_{1/(1+ρ)}(P‖Q) − θ] = min{D(V‖P) : D(V‖Q) ≤ θ}` between the
two error exponents of testing a vertex law `P` against a centre `Q`, with the divergence replaced by the radius (the
centre depends on the order) — type-II exponent `θ` ↔ the sampling rate, type-I exponent ↔ the accuracy rate — and
`e = E_sp(θ) − θ = E_V ln(dQ/dP)` is the threshold of the likelihood-ratio test, so **the shear law (the report's shift
identity, Lemma 11.60) is the Neyman–Pearson identity `D(V‖P) − D(V‖Q) = E_V ln(dQ/dP)`** (on the cube:
`KL(ρ‖p_u) − KL(ρ‖½) = uρ − Λ₁`, the report's `klBin_shift`).
(ii) **Universal coding**: `a` = Shannon capacity `= min_Q max_φ KL(π_φ‖Q)` is the redundancy–capacity theorem (Gallager
1979, Ryabko 1979, Davisson–Leon-Garcia 1980 — from memory) combined with the sample size `e^{KL(target‖proposal)}` of
importance sampling (Chatterjee–Diaconis 2018, cited by the theory report): the best single proposal for all cone
laws; §11.20 already reads `μ_H` as the Shtarkov distribution, and `C_t` is the *minimax Rényi redundancy* of the vertex
family (Yagli–Altuğ–Verdú, arXiv:1701.01103 — search snippet).  (iii) **Covering, not packing**: the fixed sample must
hit the conditional-type shells `V` with `I(M,V) ≤ θ` around an unknown label sequence, which is why `E_sp` is exact at all
rates, with no critical rate and no expurgation — as for list decoding with exponential lists (from memory).  What I
do not recognise in print, at this depth: the operational statement itself (worst-case query complexity of certifying
a normalising constant over a Lipschitz class, non-adaptive against adaptive) and the non-concavity/label-switch
phenomenon in this setting — although non-concavity of `max_M E_0(ρ,M)` in `ρ` for channels with more inputs than outputs
is textbook material (Gallager 1968, the six-input example — from memory), and the report's "label switch" is that
phenomenon.  "Not recognised", not "new".

---

## 8. Limitations of this review

* The count of evaluations of the one-level algorithm (Theorem 11.52/F7: "how large `M` gets", the count of points
  close to a level, the cost sum) was read and checked to be measure-free, not re-derived line by line; referees R7
  and R9 did that for two letters.  Nothing of the nested algorithm was simulated by anyone in this setting.
* The uniformity of the `o(n)` through `k` nested levels is on paper, as in the two-letter case.
* I did not re-run the workstream's exact joint-type sums, large brute-force runs or isoperimetric families, and did
  not read `A_REPORT.md` (Lemma 3(c), Theorem A), on which nothing reviewed here depends after the re-derivations.
* Lean: only `RenyiCentre.lean` was compiled; the other files were read at the level of statements; `scripts/audit_all.sh`
  was not run.
* Theorem 11.97(b)'s consequence for hinted algorithms (the hedged spot-check of Theorem 11.22(e)) was read, not
  re-derived.  Propositions 11.100, 11.102, 11.103 were replicated numerically where stated above and otherwise not
  reviewed (11.103(a)–(c) not at all).
* Prior art: four web searches (snippets only); the classical references are otherwise from memory and marked so.

---

## 9. Recommended corrective action

1. Add W2(c) to the theory report as Theorem 11.97(c) (M1), with the uniformity clause, and send it to a referee with
   Theorem 11.78(b); cite the file of the R10 report (m10).
2. In the proof of Theorem 11.101(b) insert the definition of an exponent function of a composition-indexed family and
   the uniformity argument (§4.6), and cite `iterates_lt_hint_add` + `GameFunction.pair` for the enumeration start (M2, m7,
   m9).
3. Restrict the dictionary sentence to `0 < θ < h` (adaptive) / `0 < θ < a` (fixed sample), say "at the exponential scale,
   in the worst case over the class", and repair the sentence on the truncated cone (m1, m2); say "maximised over the
   input law of every site type" for `E_0` (m4).
4. Use the wording of the theorem headers for what is machine-checked in the status paragraph and the README (m3).
5. Correct the slope jump (`+0.0056`), and the two constants of the isoperimetric proof (m5, m6, m8).
6. Add the hypothesis-testing and universal-coding readings to the prior-art paragraph (§7), or have workstream A1
   confirm or refute them.

---

## 10. Unresolved questions, next steps, requests

**Not settled here.**  (1) Whether the nested algorithm relative to `H` behaves as proved on any instance with more than
two letters: there is no simulation, and `Ξ_H` is not explicit.  (2) The true size of `ω_n` in W2(c) (proof:
`n^{−1/(2q_max+2)}`; evidence of the workstream: `c·ln n/n`).  (3) Concavity of `F*` for two letters — true on 500 further random sites (§6.3), unproved.
(4) Upper bounds at bounded accuracy beyond the uniform cube.  (5) Which site law is hardest for a given envelope.
(6) Whether types with vanishing fractions need separate treatment (I believe not).

**Three most promising next steps.**  (a) A finite-`n` version of W2(c): exact tail functions `Ξ_H(q)` on chains small
enough for exhaustive search, to see the error term and the extremal sets for three letters (request E1).  (b) A proof
or a counterexample for "the site function of a two-letter site is concave", i.e. "`max_p E_0(ρ,p)` is concave in `ρ` for
every binary-input binary-output channel" — a clean one-parameter statement.  (c) Writing the hinted/adaptive exponent
as a Neyman–Pearson threshold (§7(i)) suggests a direct proof of the shear law for arbitrary reference instances, and a
check against the hypothesis-testing literature for the two-phase case of §11.23, where the pair identity can fail.

**Requests.**

*To the theory division (T1).*  State and prove in the theory report: "for site types `(π_j, d_j)_{j≤m}` there is `ω_n → 0`
such that for every chain with `n` sites of these types, every real `e` and every `D ⊊ X`: `Φ_H⁺(D) ≥ e^{ne} ⟹
μ_H(D) ≥ exp(−n[R̂_{λ(n)}(e − ω_n) + ω_n])`, `λ(n)` the composition of the chain" — with the dependence of `ω_n` on
`(m, q_max, D_max, π_min)` explicit.  *(T2)* In Theorem 11.101(b) adopt (G1), (G2) of §4.6 or replace them by your own
argument; say whether `λ_j > 0` is assumed.  *(T3)* Decide the concavity question for two letters, or record the
range of the numerical evidence.

*To the engineering division (E1; a specification, not a priority).*  **Motivation:** the only isoperimetric input of
§11.26 has an unquantified error term.  **Formulation:** for a chain with product law `π` and envelope `d`, with
`ψ_H(x) = −V_n(P_x)`, `V_n(P) = min_{P′}[J_{P′} + δ(P′,P)]`, `μ_H ∝ πe^{−ψ_H}`, `s_H(y,x) = d(y,x) − ψ_H(y) + ψ_H(x)`, compute exactly
`Ξ_H(q) = max{Σ_{x∈D}μ_H(x)(e^{min_{y∉D}s_H(y,x)} − 1) : D ⊊ X, μ_H(D) ≤ q}` for all thresholds `q` that occur.  **Inputs:** the
sites `path` and `asym` of §11.26 (three letters), chains of `n = 2, 3` sites (9 and 27 points; all `2²⁷` subsets by
exhaustive enumeration with incremental updates), and two-type chains `bin`+`path` with `2·3² = 18` and `2²·3² = 36` points
(the latter by branch and bound or by restriction to unions of joint-type-and-block cells).  **Outputs:** the table
`q ↦ Ξ_H(q)` and one maximiser per `q`; the least `ω` with `n^{-1}ln Ξ_H(e^{−nθ}) ≤ R̂^{-1}(θ − ω) + ω`.  **Validation:** on the
uniform two-letter cube the result must equal Harper's function `2^{−n}E_r(n)`; the tail lemma
`E_{μ_H}(Ŵ − s)₊ ≤ s·Ξ_H(μ_H(Ŵ > s))` must hold for random members (my `t06` does this check at 36 points with the set-wise
bound).  **Stopping:** `2²⁷` subsets at most; one hour.  **Resources:** one core, under 2 GB.

---

## Appendix: how to re-run

All scripts are in `experiments/science/ws_R5/`, run from that directory with `python3 <script>`; outputs in `out/`.

| script | what | run time on the shared machine |
|---|---|---|
| `r5lib.py` | library (own implementation) | — |
| `t01_identity.py` | identity by three routes; random asymmetric sites | 5 min |
| `t02_reference_numbers.py` | the worked-example table, coarse-graining/deletion, non-additivity | 7 min |
| `t03_dictionary.py` | cube = BSC; raw Gallager/sphere packing against `S∘R̂^{-1}`; fixed-`M` forms | 11 min |
| `t04_beyond_two_letters.py`, `t04b_kink.py`, `t04c_split.py` | non-concavity, hardest site law, groupings, exact crossings | 6 min |
| `t05_evaluation_lemma.py 14` | primal test of the single-letter lemma | 6 min |
| `t06_bruteforce_orientation.py` | brute force, two types, asymmetric envelopes | 5 s |
| `t07_misc.py`, `t07b_zero_threshold.py`, `t07c_rare_third_state.py` | grid of 171 site laws; asymmetric two-letter normal form; zero residual; `n = 480`; a rare third state | 14 min |
| `t08_binary_concavity.py 500` | concavity scan for two letters | 2 min |
| `t09_lemma_Tprime.py` | Lemma 11.96 by exact enumeration | 1 s |
| `lean_check/RenyiCentre_copy.lean` | `cd /home/user/MetricChain; lake env lean <absolute path>` | 2 min |
